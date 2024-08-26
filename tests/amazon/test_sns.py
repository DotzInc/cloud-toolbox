import unittest
from unittest import mock

from cloud.amazon.sns import Publisher
from cloud.protocols import MessagePublisher


class TestMessagePublisher(unittest.TestCase):
    @mock.patch("boto3.client")
    def test_message_publisher(self, client_mock):
        response = {"MessageId": "4c6e445c-308e-46d5-90f8-aa77d29298d4"}
        cli = client_mock.return_value
        cli.publish.return_value = response

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        client_mock.assert_called_once_with("sns")

        topic = "arn:aws:sns:us-east-1:123456789012:test-topic"
        message = "test message"

        message_id = publisher.publish(topic, message)

        self.assertEqual(message_id, response["MessageId"])
        cli.publish.assert_called_once_with(TargetArn=topic, Message=message)
