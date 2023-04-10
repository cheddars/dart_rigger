# Dart API/Web Data Rigger

## Usage

### Dart API

```python
from dartrig import DartAPI

keys = [
    "{YOUR_API_KEY_01}",
    "{YOUR_API_KEY_02"
]

dart = DartAPI(keys=keys)

# Get disclosure list
dart.get_disclosure_list(end_de='20210331')
```