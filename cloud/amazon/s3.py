from typing import Any

import boto3


class Client:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.client = boto3.client("s3", *args, **kwargs)

    def upload(self, bucket_name: str, destination_filename: str, source_filename: str) -> None:
        self.client.upload_file(source_filename, bucket_name, destination_filename)

    def download(self, bucket_name: str, source_filename: str, destination_filename: str) -> None:
        self.client.download_file(bucket_name, source_filename, destination_filename)

    def generate_presigned_url(
        self,
        bucket_name: str,
        source_filename: str,
        expiration: int,
    ) -> str:
        url = self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": source_filename},
            ExpiresIn=expiration,
        )

        return url


class Uploader(Client):
    pass


class Downloader(Client):
    pass


class URLSigner(Client):
    pass
