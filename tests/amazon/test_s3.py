import unittest
from unittest import mock

from cloud.amazon.s3 import Downloader, Uploader, URLSigner
from cloud.protocols import StorageDownloader, StorageUploader


class TestStorageUploader(unittest.TestCase):
    @mock.patch("boto3.client")
    def test_storage_upload(self, client_mock):
        uploader = Uploader()

        self.assertIsInstance(uploader, StorageUploader)
        client_mock.assert_called_once_with("s3")

        bucket_name = "test-bucket"
        object_name = "test.txt"
        source_path = "/tmp/test.txt"

        uploader.upload(bucket_name, object_name, source_path)

        cli = client_mock.return_value
        cli.upload_file.assert_called_once_with(source_path, bucket_name, object_name)


class TestStorageDownloader(unittest.TestCase):
    @mock.patch("boto3.client")
    def test_storage_download(self, client_mock):
        downloader = Downloader()

        self.assertIsInstance(downloader, StorageDownloader)
        client_mock.assert_called_once_with("s3")

        bucket_name = "test-bucket"
        object_name = "test.txt"
        destination = "/tmp/test.txt"

        downloader.download(bucket_name, object_name, destination)

        cli = client_mock.return_value
        cli.download_file.assert_called_once_with(bucket_name, object_name, destination)


class TestStorageURLSigner(unittest.TestCase):
    @mock.patch("boto3.client")
    def test_storage_generate_presigned_url(self, client_mock):
        urlsigner = URLSigner()

        client_mock.assert_called_once_with("s3")

        bucket_name = "test-bucket"
        object_name = "test.txt"
        expiration = 3600

        urlsigner.generate_presigned_url(bucket_name, object_name, expiration)

        cli = client_mock.return_value
        cli.generate_presigned_url.assert_called_once_with(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
