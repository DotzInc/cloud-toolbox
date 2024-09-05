import unittest
import uuid
from unittest import mock

from cloud.amazon.sqs import Publisher
from cloud.protocols import MessagePublisher


class TestMessagePublisher(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch("boto3.client")
        self.mock = self.patcher.start()
        self.client = self.mock.return_value

    def tearDown(self):
        self.patcher.stop()

    def test_publish(self):
        response = {"MessageId": "8a70d06b-ebe7-4f63-9b89-f5e3c89d56bb"}
        self.client.send_message.return_value = response

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.mock.assert_called_once_with("sqs")

        queue = "https://sqs.us-east-1.amazonaws.com/123456789012/test-queue"
        message = "test message"
        message_id = publisher.publish(queue, message)

        self.assertEqual(message_id, response["MessageId"])
        self.client.send_message.assert_called_once_with(QueueUrl=queue, MessageBody=message)

    def test_publish_with_attributes(self):
        response = {"MessageId": "53af3eae-2346-4c17-bc0d-73d738306119"}
        self.client.send_message.return_value = response

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.mock.assert_called_once_with("sqs")

        queue = "https://sqs.us-east-1.amazonaws.com/123456789012/test-queue"
        message = "test message"
        attributes = {"foo": "bar"}
        message_id = publisher.publish(queue, message, **attributes)

        self.assertEqual(message_id, response["MessageId"])
        self.client.send_message.assert_called_once_with(
            QueueUrl=queue,
            MessageBody=message,
            MessageAttributes=attributes,
        )

    def test_publish_with_ordering(self):
        response = {"MessageId": "102aff13-77e8-4a4d-8e1c-d271e7b80285"}
        self.client.send_message.return_value = response

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.mock.assert_called_once_with("sqs")

        queue = "https://sqs.us-east-1.amazonaws.com/123456789012/test-queue"
        message = "test message"
        group = "test"
        deduplication_id = uuid.uuid4()

        with mock.patch("uuid.uuid4", lambda: deduplication_id):
            message_id = publisher.publish(queue, message, group)

        self.assertEqual(message_id, response["MessageId"])
        self.client.send_message.assert_called_once_with(
            QueueUrl=queue,
            MessageBody=message,
            MessageGroupId=group,
            MessageDeduplicationId=str(deduplication_id),
        )
