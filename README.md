# Cloud Toolbox

![Tests](https://github.com/DotzInc/cloud-toolbox/actions/workflows/tests.yml/badge.svg?event=push)
![PyPI - Version](https://img.shields.io/pypi/v/cloudtoolbox)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloudtoolbox)

Decouple your applications from cloud providers with carefully crafted service interfaces.

## Requirements

* Python 3.8+

## Installation

To install Cloud Toolbox, use pip:

```sh
pip install cloudtoolbox
```

### Extras

Cloud Toolbox offers the following optional dependencies for easy installation of provider SDKs:

* `cloudtoolbox[amazon]` - Installs the Amazon AWS SDK.
* `cloudtoolbox[google]` - Installs the Google Cloud SDK.
* `cloudtoolbox[all]` - Installs SDKs for both providers.

## Example

Uploading a file to Google Cloud Storage.

```python
from cloud import factory
from cloud.google.storage import Uploader

FileUploader = factory.storage_uploader(Uploader)

bucket = "my-bucket"
filename = "notes.txt"
filepath = f"/path/to/{filename}"

uploader = FileUploader()
uploader.upload(bucket, filename, filepath)
```

Switching from Cloud Storage to Amazon S3.

```python
# Replace this import
from cloud.google.storage import Uploader

# For this one
from cloud.amazon.s3 import Uploader
```
