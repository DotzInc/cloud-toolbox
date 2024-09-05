import uuid
from typing import Any

import boto3


class Publisher:
    def __init__(self, *args: Any, **kwargs: Any):
        self.client = boto3.client("sns", *args, **kwargs)

    def publish(self, recipient: str, message: str, group: str = "", **attrs: Any) -> str:
        kwargs = {}

        if group:
            kwargs["MessageGroupId"] = group
            kwargs["MessageDeduplicationId"] = str(uuid.uuid4())

        if attrs:
            kwargs["MessageAttributes"] = attrs

        response = self.client.publish(TargetArn=recipient, Message=message, **kwargs)
        return response["MessageId"]
