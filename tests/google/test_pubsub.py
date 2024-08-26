import unittest
from unittest import mock

from cloud.google.pubsub import Publisher
from cloud.protocols import MessagePublisher


class TestMessagePublisher(unittest.TestCase):
    @mock.patch("google.cloud.pubsub_v1.PublisherClient")
    def test_message_publisher(self, client_mock):
        result = "bd02bec5-ac5f-429b-8f64-8cde17596d57"
        cli = client_mock.return_value
        future = cli.publish.return_value
        future.result.return_value = result

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        client_mock.assert_called_once_with()

        topic = "projects/test-project/topics/test-topic"
        message = "test message"

        message_id = publisher.publish(topic, message)

        self.assertEqual(message_id, result)
        cli.publish.assert_called_once_with(topic, data=message.encode())
