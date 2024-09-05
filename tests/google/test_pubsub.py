import unittest
from unittest import mock

from google.cloud.pubsub_v1.types import PublisherOptions

from cloud.google.pubsub import OrderedPublisher, Publisher
from cloud.protocols import MessagePublisher


class TestMessagePublisher(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch("google.cloud.pubsub_v1.PublisherClient")
        self.mock = self.patcher.start()
        self.client = self.mock.return_value
        self.future = self.client.publish.return_value

    def tearDown(self):
        self.patcher.stop()

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
        message_id = publisher.publish(topic, message, **attributes)

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
        message_id = publisher.publish(topic, message, group)

        self.assertEqual(message_id, result)
        self.client.publish.assert_called_once_with(
            topic,
            data=message.encode(),
            ordering_key=group,
        )
