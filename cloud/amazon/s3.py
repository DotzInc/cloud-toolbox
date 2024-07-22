from enum import Enum
from typing import Any

import boto3


class ClientMethodName(str, Enum):
    GET_OBJECT = "get_object"
    LIST_OBJECTS = "list_objects"
    LIST_OBJECTS_V2 = "list_objects_v2"
    PUT_OBJECT = "put_object"
    DELETE_OBJECT = "delete_object"
    HEAD_OBJECT = "head_object"
    COPY_OBJECT = "copy_object"


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
        client_method_name: ClientMethodName,
    ) -> str:
        url = self.client.generate_presigned_url(
            ClientMethod=client_method_name,
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
