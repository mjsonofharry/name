# name
Python client for Name.com API.

## Installation

```
pip install git+https://github.com/mjsonofharry/name.git@v0.0.1
```

## Usage

```python
from name.client import NameClient
from name.record import Record

name_client = NameClient(username="", password="")
name_client.update_record(record=Record(
    type="A",
    host="",
    domain: "google.com",
    ttl: 129600
))
```
