import unittest
from unittest import mock

from cloud.amazon.sqs import Publisher
from cloud.protocols import MessagePublisher


class TestMessagePublisher(unittest.TestCase):
    @mock.patch("boto3.client")
    def test_message_publisher(self, client_mock):
        response = {"MessageId": "8a70d06b-ebe7-4f63-9b89-f5e3c89d56bb"}
        cli = client_mock.return_value
        cli.send_message.return_value = response

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        client_mock.assert_called_once_with("sqs")

        queue = "https://sqs.us-east-1.amazonaws.com/123456789012/test-queue"
        message = "test message"

        message_id = publisher.publish(queue, message)

        self.assertEqual(message_id, response["MessageId"])
        cli.send_message.assert_called_once_with(QueueUrl=queue, MessageBody=message)
