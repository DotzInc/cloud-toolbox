from typing import Any

import boto3


class Publisher:
    def __init__(self, *args: Any, **kwargs: Any):
        self.client = boto3.client("sqs", *args, **kwargs)

    def publish(self, recipient: str, message: str, **attrs: Any) -> str:
        response = self.client.send_message(QueueUrl=recipient, MessageBody=message, **attrs)
        return response["MessageId"]
