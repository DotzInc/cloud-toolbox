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

## Publishing to Google Pub/Sub

Use `Publisher` as a context manager to reuse its client while publishing and
close it automatically when the context exits. The recipient is the fully
qualified Pub/Sub topic name, and `publish` returns the published message ID.

```python
from cloud.google.pubsub import Publisher

topic = "projects/my-project/topics/my-topic"

with Publisher() as publisher:
    message_id = publisher.publish(topic, "Hello, Pub/Sub!")
    print(message_id)
```

Pass message attributes with `attrs`:

```python
with Publisher() as publisher:
    message_id = publisher.publish(
        topic,
        "Order created",
        attrs={"event_type": "order.created", "order_id": "1234"},
    )
```

For ordered publishing, use `OrderedPublisher` and provide the ordering key
with `group`:

```python
from cloud.google.pubsub import OrderedPublisher

with OrderedPublisher() as publisher:
    message_id = publisher.publish(
        topic,
        "Order updated",
        group="order-1234",
    )
```

The `message_publisher` factory can also create the publisher through the
common message-publisher interface:

```python
from cloud import factory
from cloud.google.pubsub import Publisher

PublisherFactory = factory.message_publisher(Publisher)

with PublisherFactory() as publisher:
    message_id = publisher.publish(topic, "Hello, Pub/Sub!")
```
