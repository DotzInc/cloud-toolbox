from types import TracebackType
from typing import Any, Mapping, Optional, Type

from google.cloud import pubsub_v1


class Publisher:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.client = pubsub_v1.PublisherClient(*args, **kwargs)
        self._closed = False

    def close(self) -> None:
        if self._closed:
            return

        self._closed = True
        try:
            self.client.stop()
        finally:
            self.client.transport.close()

    def __enter__(self) -> "Publisher":
        if self._closed:
            raise RuntimeError("Publisher is closed")
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    def publish(
        self,
        recipient: str,
        message: str,
        /,
        *,
        group: str = "",
        attrs: Optional[Mapping[str, Any]] = None,
    ) -> str:
        if self._closed:
            raise RuntimeError("Publisher is closed")

        kwargs = attrs or {}
        future = self.client.publish(recipient, data=message.encode(), ordering_key=group, **kwargs)
        return future.result()


class OrderedPublisher(Publisher):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        opts = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
        super().__init__(*args, publisher_options=opts, **kwargs)
