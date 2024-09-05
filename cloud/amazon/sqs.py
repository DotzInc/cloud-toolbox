import uuid
from typing import Any, Mapping, Optional

import boto3

from cloud.amazon import helpers


class Publisher:
    def __init__(self, *args: Any, **kwargs: Any):
        self.client = boto3.client("sqs", *args, **kwargs)

    def publish(
        self,
        recipient: str,
        message: str,
        /,
        *,
        group: str = "",
        attrs: Optional[Mapping[str, Any]] = None,
    ) -> str:
        kwargs = {}

        if group:
            kwargs["MessageGroupId"] = group
            kwargs["MessageDeduplicationId"] = str(uuid.uuid4())

        if attrs:
            kwargs["MessageAttributes"] = helpers.build_attributes(attrs)

        response = self.client.send_message(QueueUrl=recipient, MessageBody=message, **kwargs)
        return response["MessageId"]
