import datetime
from typing import Any

from google.cloud import storage


class Client:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.client = storage.Client(*args, **kwargs)

    def upload(self, bucket_name: str, destination_filename: str, source_filename: str) -> None:
        blob = self.client.bucket(bucket_name).blob(destination_filename)
        blob.upload_from_filename(source_filename)

    def download(self, bucket_name: str, source_filename: str, destination_filename: str) -> None:
        blob = self.client.bucket(bucket_name).blob(source_filename)
        blob.download_to_filename(destination_filename)

    def generate_presigned_url(
        self,
        bucket_name: str,
        source_filename: str,
        expiration: int,
    ) -> str:
        blob = self.client.bucket(bucket_name).blob(source_filename)
        url = blob.generate_signed_url(
            expiration=datetime.timedelta(seconds=expiration),
            version="v4",
        )
        return url


class Uploader(Client):
    pass


class Downloader(Client):
    pass


class URLSigner(Client):
    pass
