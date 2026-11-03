import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import mock

from google.cloud.pubsub_v1.types import PublisherOptions

from cloud.google.pubsub import OrderedPublisher, Publisher
from cloud.protocols import MessagePublisher


class TestMessagePublisher(unittest.TestCase):
    def setUp(self):
        Publisher._clients.clear()
        self.patcher = mock.patch("google.cloud.pubsub_v1.PublisherClient")
        self.mock = self.patcher.start()
        self.client = self.mock.return_value
        self.future = self.client.publish.return_value

    def tearDown(self):
        self.patcher.stop()
        Publisher._clients.clear()

    def test_publish(self):
        result = "bd02bec5-ac5f-429b-8f64-8cde17596d57"
        self.future.result.return_value = result

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.mock.assert_called_once_with()

        topic = "projects/test-project/topics/test-topic"
        message = "test message"
        message_id = publisher.publish(topic, message)

        self.assertEqual(message_id, result)
        self.client.publish.assert_called_once_with(topic, data=message.encode(), ordering_key="")

    def test_publish_with_attributes(self):
        result = "8a26e938-0f1d-41a8-be91-9815f2003cf7"
        self.future.result.return_value = result

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.mock.assert_called_once_with()

        topic = "projects/test-project/topics/test-topic"
        message = "test message"
        attributes = {"foo": "bar"}
        message_id = publisher.publish(topic, message, attrs=attributes)

        self.assertEqual(message_id, result)
        self.client.publish.assert_called_once_with(
            topic,
            data=message.encode(),
            ordering_key="",
            **attributes,
        )

    def test_publish_with_ordering(self):
        result = "51c8af51-833a-4f1a-b90c-195422cf845a"
        self.future.result.return_value = result
        opts = PublisherOptions(enable_message_ordering=True)

        publisher = OrderedPublisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.mock.assert_called_once_with(publisher_options=opts)

        topic = "projects/test-project/topics/test-topic"
        message = "test message"
        group = "test"
        message_id = publisher.publish(topic, message, group=group)

        self.assertEqual(message_id, result)
        self.client.publish.assert_called_once_with(
            topic,
            data=message.encode(),
            ordering_key=group,
        )

    def test_reuses_client_across_publishers(self):
        first = Publisher()
        second = Publisher()

        self.assertIsNot(first, second)
        self.assertIs(first.client, second.client)
        self.mock.assert_called_once_with()

    def test_reuses_client_across_threads(self):
        barrier = Barrier(8)

        def create():
            barrier.wait()
            return Publisher().client

        with ThreadPoolExecutor(max_workers=8) as executor:
            clients = list(executor.map(lambda _: create(), range(8)))

        self.assertEqual(len({id(client) for client in clients}), 1)
        self.mock.assert_called_once_with()

    def test_separates_clients_by_arguments(self):
        self.mock.side_effect = lambda *args, **kwargs: mock.Mock()

        default = Publisher()
        ordered = OrderedPublisher()

        self.assertIsNot(default.client, ordered.client)
        self.assertIs(ordered.client, OrderedPublisher().client)
        self.assertEqual(self.mock.call_count, 2)

    def test_creates_new_client_for_unhashable_arguments(self):
        self.mock.side_effect = lambda *args, **kwargs: mock.Mock()
        options = {"enable_message_ordering": True}

        first = Publisher(publisher_options=options)
        second = Publisher(publisher_options=options)

        self.assertIsNot(first.client, second.client)
        self.assertEqual(self.mock.call_count, 2)

    def test_creates_new_client_after_fork(self):
        self.mock.side_effect = lambda *args, **kwargs: mock.Mock()
        parent = Publisher()

        with mock.patch("os.getpid", return_value=-1):
            child = Publisher()

        self.assertIsNot(parent.client, child.client)
        self.assertEqual(self.mock.call_count, 2)
