import datetime
import unittest
from unittest import mock

from cloud.google.storage import Downloader, Uploader, URLSigner
from cloud.protocols import StorageDownloader, StorageUploader, StorageURLSigner


class TestStorageUploader(unittest.TestCase):
    @mock.patch("google.cloud.storage.Client")
    def test_storage_uploader(self, client_mock):
        uploader = Uploader()

        self.assertIsInstance(uploader, StorageUploader)
        client_mock.assert_called_once_with()

        bucket_name = "test-bucket"
        object_name = "test.txt"
        source_path = "/tmp/test.txt"

        uploader.upload(bucket_name, object_name, source_path)

        cli = client_mock.return_value
        cli.bucket.assert_called_once_with(bucket_name)

        bucket = cli.bucket.return_value
        bucket.blob.assert_called_once_with(object_name)

        blob = bucket.blob.return_value
        blob.upload_from_filename.assert_called_once_with(source_path)


class TestStorageDownloader(unittest.TestCase):
    @mock.patch("google.cloud.storage.Client")
    def test_storage_downloader(self, client_mock):
        downloader = Downloader()

        self.assertIsInstance(downloader, StorageDownloader)
        client_mock.assert_called_once_with()

        bucket_name = "test-bucket"
        object_name = "test.txt"
        destination = "/tmp/test.txt"

        downloader.download(bucket_name, object_name, destination)

        cli = client_mock.return_value
        cli.bucket.assert_called_once_with(bucket_name)

        bucket = cli.bucket.return_value
        bucket.blob.assert_called_once_with(object_name)

        blob = bucket.blob.return_value
        blob.download_to_filename.assert_called_once_with(destination)


class TestStorageURLSigner(unittest.TestCase):
    @mock.patch("google.cloud.storage.Client")
    @mock.patch("google.auth.default")
    def test_storage_urlsigner(self, default_mock, client_mock):
        default_mock.return_value = (mock.MagicMock(token=None), None)
        urlsigner = URLSigner()

        self.assertIsInstance(urlsigner, StorageURLSigner)
        client_mock.assert_called_once_with()

        bucket_name = "test-bucket"
        object_name = "test.txt"
        expiration = 60
        client_method_name = "GET"

        urlsigner.generate_presigned_url(bucket_name, object_name)

        cli = client_mock.return_value
        cli.bucket.assert_called_once_with(bucket_name)

        bucket = cli.bucket.return_value
        bucket.blob.assert_called_once_with(object_name)

        blob = bucket.blob.return_value
        blob.generate_signed_url.assert_called_once_with(
            version="v4",
            service_account_email=mock.ANY,
            access_token=None,
            expiration=datetime.timedelta(minutes=expiration),
            method=client_method_name,
        )
