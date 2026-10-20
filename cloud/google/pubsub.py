import os
from threading import Lock
from typing import Any, Dict, Hashable, Mapping, Optional

from google.cloud import pubsub_v1


class Publisher:
    _clients: Dict[Hashable, pubsub_v1.PublisherClient] = {}
    _lock = Lock()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.client = self._shared_client(*args, **kwargs)

    @classmethod
    def _shared_client(cls, *args: Any, **kwargs: Any) -> pubsub_v1.PublisherClient:
        try:
            key = (os.getpid(), args, frozenset(kwargs.items()))
            hash(key)
        except TypeError:
            return pubsub_v1.PublisherClient(*args, **kwargs)

        client = cls._clients.get(key)
        if client is None:
            with cls._lock:
                client = cls._clients.get(key)
                if client is None:
                    client = pubsub_v1.PublisherClient(*args, **kwargs)
                    cls._clients[key] = client
        return client

    def publish(
        self,
        recipient: str,
        message: str,
        /,
        *,
        group: str = "",
        attrs: Optional[Mapping[str, Any]] = None,
    ) -> str:
        kwargs = attrs or {}
        future = self.client.publish(recipient, data=message.encode(), ordering_key=group, **kwargs)
        return future.result()


class OrderedPublisher(Publisher):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        opts = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
        super().__init__(*args, publisher_options=opts, **kwargs)
