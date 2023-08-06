[![Version](https://img.shields.io/pypi/v/tcclient.svg?style=plastic&logo=appveyor)](https://img.shields.io/pypi/v/tcclient.svg)


# tcclient

Cross-platform tool to work with the TeamCity using REST API. The main goal is to run TeamCity configuration remotely,
for example, from a Telegram bot.

## Installation
For most users, the recommended method to install is via pip:
```cmd
pip install tcclient
```
## Import
```python
from tcclient import TCRestClient
```
---
## Usage
#### Command from usual user:
```python
import os
from tcclient import TCRestClient

token = os.environ['TOKEN']
base_url = "https://tc.test.local:8080"
client = TCRestClient(base_url=base_url, token=token)

projects = client.get_all_projects()
print(projects.json())
```

---

## Changelog

##### 0.0.1.post1 (28.03.2021)

- minor fixes (typo and github link)

##### 0.0.1 (28.03.2021)

- initial commit
