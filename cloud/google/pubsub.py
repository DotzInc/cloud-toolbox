from typing import Any

from google.cloud import pubsub_v1


class Publisher:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.client = pubsub_v1.PublisherClient(*args, **kwargs)

    def publish(self, recipient: str, message: str, group: str = "", **attrs: Any) -> str:
        future = self.client.publish(recipient, data=message.encode(), ordering_key=group, **attrs)
        return future.result()


class OrderedPublisher(Publisher):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        opts = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
        super().__init__(*args, publisher_options=opts, **kwargs)
