from typing import Any

import boto3


class Publisher:
    def __init__(self, *args: Any, **kwargs: Any):
        self.client = boto3.client("sns", *args, **kwargs)

    def publish(self, recipient: str, message: str, **attrs: Any) -> str:
        response = self.client.publish(TargetArn=recipient, Message=message, **attrs)
        return response["MessageId"]
