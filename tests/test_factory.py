import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
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

    @mock.patch("google.cloud.pubsub_v1.PublisherClient")
    def test_google_ordered_publisher(self, _):
        OrderedPublisher = factory.message_publisher(pubsub.OrderedPublisher)
        publisher = OrderedPublisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.assertIsInstance(publisher, pubsub.OrderedPublisher)

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


class TestSharedMessagePublisherFactory(unittest.TestCase):
    @mock.patch("google.cloud.pubsub_v1.PublisherClient")
    def test_creates_publisher_lazily(self, client):
        get_publisher = factory.shared_message_publisher(pubsub.Publisher)

        client.assert_not_called()
        publisher = get_publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.assertIsInstance(publisher, pubsub.Publisher)
        client.assert_called_once_with()

    @mock.patch("google.cloud.pubsub_v1.PublisherClient")
    def test_reuses_publisher_across_calls(self, client):
        get_publisher = factory.shared_message_publisher(pubsub.Publisher)

        self.assertIs(get_publisher(), get_publisher())
        client.assert_called_once_with()

    @mock.patch("google.cloud.pubsub_v1.PublisherClient")
    def test_reuses_publisher_across_threads(self, client):
        get_publisher = factory.shared_message_publisher(pubsub.Publisher)
        barrier = Barrier(8)

        def call():
            barrier.wait()
            return get_publisher()

        with ThreadPoolExecutor(max_workers=8) as executor:
            publishers = list(executor.map(lambda _: call(), range(8)))

        self.assertEqual(len({id(item) for item in publishers}), 1)
        client.assert_called_once_with()

    @mock.patch("google.cloud.pubsub_v1.PublisherClient")
    def test_forwards_arguments_to_publisher(self, client):
        factory.shared_message_publisher(pubsub.OrderedPublisher, "arg")()

        self.assertEqual(client.call_args.args, ("arg",))

    @mock.patch("google.cloud.pubsub_v1.PublisherClient")
    def test_publishers_are_independent_per_factory(self, _):
        first = factory.shared_message_publisher(pubsub.Publisher)
        second = factory.shared_message_publisher(pubsub.Publisher)

        self.assertIsNot(first(), second())

    def test_publisher_protocol_validation(self):
        error = "NotMessagePublisher does not implement MessagePublisher protocol"

        with self.assertRaisesRegex(AssertionError, error):
            factory.shared_message_publisher(NotMessagePublisher)
