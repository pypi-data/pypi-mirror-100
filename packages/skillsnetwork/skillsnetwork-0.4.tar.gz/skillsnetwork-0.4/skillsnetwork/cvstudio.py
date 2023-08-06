import os
import requests
import json
from datetime import datetime, date
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import pandas as pd
import torch
# import torchvision.models as models
# from torch.utils.data import Dataset, DataLoader,random_split
# from torch.optim import lr_scheduler
from torch.utils.data import Dataset
from torchvision import transforms
from tqdm import tqdm

def default(o):
    if isinstance(o, (date, datetime)):
        return o.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")

class CVStudio(object):
    def __init__(self, token=None, ibm_api_key_id=None, base_url=None):
        if token == None:
            self.token = os.environ.get('CV_STUDIO_TOKEN')
            if self.token == None:
                raise Exception('need to pass valid token or set CV_STUDIO_TOKEN environment variable')
        else:
            self.token = token

        if ibm_api_key_id == None:
            self.ibm_api_key_id = os.environ.get('IBMCLOUD_API_KEY')
            if self.ibm_api_key_id == None:
                raise Exception('need to pass valid ibm_api_key_id or set IBMCLOUD_API_KEY environment variable')
        else:
            self.ibm_api_key_id = ibm_api_key_id

        if base_url == None:
            self.base_url = os.environ.get('CV_STUDIO_BASE_URL', 'https://vision.skills.network')
        else:
            self.base_url = base_url

        self.setup()

    def setup(self):
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        
        x = requests.post(self.base_url + '/api/cos_credentials', headers=headers)

        if x.ok:
            item = json.loads(x.text)
            
            self.endpoint = item['endpoint']
            self.bucket = item['bucket']

            self.cos = ibm_boto3.client("s3",
                ibm_api_key_id=self.ibm_api_key_id,
                ibm_service_instance_id=self.ibm_api_key_id,
                config=Config(signature_version="oauth"),
                endpoint_url=self.endpoint)

        else:
            print("Failed to setup CV Studio client")

        return x

    def download_file_cos(self, key):
        try:
            local_file_name=os.path.join(os.getcwd(), key)
            res=self.cos.download_file(Bucket=self.bucket, Key=key, Filename=local_file_name)
        except Exception as e:
            print('Exception', e)
        else:
            print('File Downloaded')

    def get_annotations(self):
        try:
            return json.loads(self.cos.get_object(Bucket=self.bucket, Key='_annotations.json')['Body'].read())
        except Exception as e:
            print('Exception', e)
    
    def downloadAll(self):
        for image in tqdm(self.get_annotations()['annotations'].keys()):
            self.download_file_cos(image)
    
    def getDataset(self, transform=None):
        dataset=Dataset(annotations=self.get_annotations(), bucket_name=self.bucket, transform=transform)
        return dataset
    
    def uploadModel(self, key, details={}):
        self.upload_file_cos(key)
        details['filename'] = key
        self.report(model=details)

    def upload_file_cos(self, filename):
        try:
            res=self.cos.upload_file(filename, self.bucket, os.path.basename(filename))
        except Exception as e:
            print('Exception', e)
        else:
            print('File Uploaded')
    
    def report(self, started=None, completed=None, url=None, parameters=None, accuracy=None, model=None):
        data = {}

        if started is not None:
            data['started'] = started
        
        if completed is not None:
            data['completed'] = completed

        if parameters is not None:
            data['parameters'] = parameters

        if accuracy is not None:
            data['accuracy'] = accuracy

        if model is not None:
            data['model'] = model

        if url is not None:
            data['url'] = url
        
        if len(data) == 0:
            raise Exception('Nothing to report')

        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        
        x = requests.post(self.base_url + '/api/report', headers=headers, data=json.dumps(data, default=default))

        return x

    def ping(self):
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        
        x = requests.post(self.base_url + '/api/ping', headers=headers)

        return x


class Dataset(Dataset):

    def __init__(self, annotations=None, bucket_name=None, transform=None):
        self.transform=transform
        if self.transform is None:
            self.setDefaultTransform()

        problem_type=annotations['type']
        
        if problem_type != 'classification':
            raise Exception('Can only get Dataset of Classification models')
        
        labels_types=annotations['labels']
        
        labels_filename=os.path.join(os.getcwd(),bucket_name+"_lables.csv")

        if os.path.exists(labels_filename):
            self.data=pd.read_csv(labels_filename)
        else:
            data_={'label':[],'y':[],'file_name':[],'key':[]}
#             print('HERE')
#             print(annotations.items())
            for key,label_dict in annotations['annotations'].items():                
                label=label_dict[0]['label']

                data_['label'].append(label)
                data_['y'].append(labels_types.index(label))
                data_['key'].append(key)
                data_['file_name'].append(os.path.join(os.getcwd(),key))

            self.data=pd.DataFrame(data_)
            self.data.to_csv(labels_filename)
        
        self.n_classes=len(self.data['y'].unique())

    def setDefaultTransform(self):
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.RandomHorizontalFlip(),
                transforms.RandomRotation(degrees=5),
                transforms.ToTensor(),
                transforms.Normalize(mean, std)])

    def __len__(self):
        return self.data.shape[0]

    def __getitem__(self, idx):
        image=Image.open(self.data.loc[idx, 'file_name'])
        y=self.data.loc[idx,'y']
        if self.transform:
            image= self.transform(image)
        
        return image, y
