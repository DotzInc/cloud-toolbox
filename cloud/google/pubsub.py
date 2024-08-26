from typing import Any

from google.cloud import pubsub_v1


class Publisher:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.client = pubsub_v1.PublisherClient(*args, **kwargs)

    def publish(self, recipient: str, message: str, **attrs: Any) -> str:
        future = self.client.publish(recipient, data=message.encode(), **attrs)
        return future.result()
