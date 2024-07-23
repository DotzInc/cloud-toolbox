import unittest
from unittest import mock

from cloud import factory
from cloud.amazon import s3, sns, sqs
from cloud.google import pubsub, storage
from cloud.protocols import MessagePublisher, StorageDownloader, StorageUploader, StorageURLSigner


class NotStorageUploader:
    def upload_file(self):
        pass


class NotStorageDownloader:
    def download_file(self):
        pass


class NotStorageURLSigner:
    def sign_url(self):
        pass


class DummyStorageURLSigner:
    def generate_presigned_url(
        self,
        bucket_name: str,
        source_filename: str,
        expiration: int,
    ) -> str:
        return ""


class NotMessagePublisher:
    def send_message(self):
        pass


class TestStorageUploaderFactory(unittest.TestCase):
    @mock.patch("google.cloud.storage.Client")
    def test_google_uploader(self, _):
        Uploader = factory.storage_uploader(storage.Uploader)
        uploader = Uploader()

        self.assertIsInstance(uploader, StorageUploader)
        self.assertIsInstance(uploader, storage.Uploader)

    @mock.patch("boto3.client")
    def test_amazon_uploader(self, _):
        Uploader = factory.storage_uploader(s3.Uploader)
        uploader = Uploader()

        self.assertIsInstance(uploader, StorageUploader)
        self.assertIsInstance(uploader, s3.Uploader)

    def test_uploader_protocol_validation(self):
        error = "NotStorageUploader does not implement StorageUploader protocol"

        with self.assertRaisesRegex(AssertionError, error):
            factory.storage_uploader(NotStorageUploader)  # type: ignore


class TestStorageDownloaderFactory(unittest.TestCase):
    @mock.patch("google.cloud.storage.Client")
    def test_google_downloader(self, _):
        Downloader = factory.storage_downloader(storage.Downloader)
        downloader = Downloader()

        self.assertIsInstance(downloader, StorageDownloader)
        self.assertIsInstance(downloader, storage.Downloader)

    @mock.patch("boto3.client")
    def test_amazon_downloader(self, _):
        Downloader = factory.storage_downloader(s3.Downloader)
        downloader = Downloader()

        self.assertIsInstance(downloader, StorageDownloader)
        self.assertIsInstance(downloader, s3.Downloader)

    def test_downloader_protocol_validation(self):
        error = "NotStorageDownloader does not implement StorageDownloader protocol"

        with self.assertRaisesRegex(AssertionError, error):
            factory.storage_downloader(NotStorageDownloader)  # type: ignore


class TestStorageURLSigner(unittest.TestCase):
    def test_urlsigner(self):
        URLSigner = factory.storage_urlsigner(DummyStorageURLSigner)
        urlsigner = URLSigner()

        self.assertIsInstance(urlsigner, StorageURLSigner)
        self.assertIsInstance(urlsigner, DummyStorageURLSigner)

    def test_urlsigner_protocol_validation(self):
        error = "NotStorageURLSigner does not implement StorageURLSigner protocol"

        with self.assertRaisesRegex(AssertionError, error):
            factory.storage_urlsigner(NotStorageURLSigner)  # type: ignore


class TestMessagePublisherFactory(unittest.TestCase):
    @mock.patch("google.cloud.pubsub_v1.PublisherClient")
    def test_google_publisher(self, _):
        Publisher = factory.message_publisher(pubsub.Publisher)
        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.assertIsInstance(publisher, pubsub.Publisher)

    @mock.patch("boto3.client")
    def test_amazon_publisher(self, _):
        for cls in (sns.Publisher, sqs.Publisher):
            with self.subTest(class_name=cls.__name__):
                Publisher = factory.message_publisher(cls)
                publisher = Publisher()

                self.assertIsInstance(publisher, MessagePublisher)
                self.assertIsInstance(publisher, cls)

    def test_publisher_protocol_validation(self):
        error = "NotMessagePublisher does not implement MessagePublisher protocol"

        with self.assertRaisesRegex(AssertionError, error):
            factory.message_publisher(NotMessagePublisher)  # type: ignore
