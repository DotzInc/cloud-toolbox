from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class StorageUploader(Protocol):
    def upload(self, bucket_name: str, destination_filename: str, source_filename: str) -> None: ...


@runtime_checkable
class StorageDownloader(Protocol):
    def download(
        self, bucket_name: str, source_filename: str, destination_filename: str
    ) -> None: ...


@runtime_checkable
class StorageURLSigner(Protocol):
    def generate_presigned_url(
        self,
        bucket_name: str,
        source_filename: str,
        expiration: int,
    ) -> str: ...


@runtime_checkable
class MessagePublisher(Protocol):
    def publish(self, recipient: str, message: str, **attrs: Any) -> str: ...
