from typing import Any, Callable, Type

from cloud.protocols import MessagePublisher, StorageDownloader, StorageUploader, StorageURLSigner

error_message = "%(class)s does not implement %(protocol)s protocol"


def storage_uploader(
    uploader_class: Type[StorageUploader], *args: Any, **kwargs: Any
) -> Callable[[], StorageUploader]:
    error = error_message % {"class": uploader_class.__name__, "protocol": "StorageUploader"}
    assert issubclass(uploader_class, StorageUploader), error

    def maker() -> StorageUploader:
        return uploader_class(*args, **kwargs)

    return maker


def storage_downloader(
    downloader_class: Type[StorageDownloader], *args: Any, **kwargs: Any
) -> Callable[[], StorageDownloader]:
    error = error_message % {"class": downloader_class.__name__, "protocol": "StorageDownloader"}
    assert issubclass(downloader_class, StorageDownloader), error

    def maker() -> StorageDownloader:
        return downloader_class(*args, **kwargs)

    return maker


def storage_urlsigner(
    urlsigner_class: Type[StorageURLSigner], *args: Any, **kwargs: Any
) -> Callable[[], StorageURLSigner]:
    error = error_message % {"class": urlsigner_class.__name__, "protocol": "StorageURLSigner"}
    assert issubclass(urlsigner_class, StorageURLSigner), error

    def maker() -> StorageURLSigner:
        return urlsigner_class(*args, **kwargs)

    return maker


def message_publisher(
    publisher_class: Type[MessagePublisher], *args: Any, **kwargs: Any
) -> Callable[[], MessagePublisher]:
    error = error_message % {"class": publisher_class.__name__, "protocol": "MessagePublisher"}
    assert issubclass(publisher_class, MessagePublisher), error

    def maker() -> MessagePublisher:
        return publisher_class(*args, **kwargs)

    return maker
