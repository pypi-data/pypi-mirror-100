# Skills Network Python Library

## install
```
pip install -y skillsnetwork
```

## Uninstall
```
pip uninstall -y skillsnetwork
```

## cvstudio

### Environment Variables
- `CV_STUDIO_TOKEN`
- `CV_STUDIO_BASE_URL`

### Python Code example
```
from datetime import datetime
import skillsnetwork.cvstudio
cvstudio = skillsnetwork.cvstudio.CVStudio('token')

cvstudio.report(started=datetime.now(), completed=datetime.now())

cvstudio.report(url="http://vision.skills.network")
```

### CLI example
```
# export CV_STUDIO_TOKEN="<token>"
# export CV_STUDIO_BASE_URL="<baseurl>"

cvstudio_report exampleTrainingRun.json
```

## Development:

- Build:
```
python3 -m pip install --upgrade build
python3 -m build
```

- Install (for testing):
```
version=0.3
python3 -m pip install dist/skillsnetwork-$version-py3-none-any.whl --force
```

- Publish:
```
python3 -m pip install --user --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```