import unittest
import uuid
from unittest import mock

from cloud.amazon.sns import Publisher
from cloud.protocols import MessagePublisher


class TestMessagePublisher(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch("boto3.client")
        self.mock = self.patcher.start()
        self.client = self.mock.return_value

    def tearDown(self):
        self.patcher.stop()

    def test_publish(self):
        response = {"MessageId": "4c6e445c-308e-46d5-90f8-aa77d29298d4"}
        self.client.publish.return_value = response

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.mock.assert_called_once_with("sns")

        topic = "arn:aws:sns:us-east-1:123456789012:test-topic"
        message = "test message"
        message_id = publisher.publish(topic, message)

        self.assertEqual(message_id, response["MessageId"])
        self.client.publish.assert_called_once_with(TargetArn=topic, Message=message)

    def test_publish_with_attributes(self):
        response = {"MessageId": "fc0b5cd2-abce-443f-8e8f-5c99f463b9cd"}
        self.client.publish.return_value = response

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.mock.assert_called_once_with("sns")

        topic = "arn:aws:sns:us-east-1:123456789012:test-topic"
        message = "test message"
        attributes = {"foo": "bar"}
        message_id = publisher.publish(topic, message, **attributes)

        self.assertEqual(message_id, response["MessageId"])
        self.client.publish.assert_called_once_with(
            TargetArn=topic,
            Message=message,
            MessageAttributes=attributes,
        )

    def test_publish_with_ordering(self):
        response = {"MessageId": "32672f88-e43a-4ece-8240-e2db56da2cfc"}
        self.client.publish.return_value = response

        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.mock.assert_called_once_with("sns")

        topic = "arn:aws:sns:us-east-1:123456789012:test-topic.fifo"
        message = "test message"
        group = "test"
        deduplication_id = uuid.uuid4()

        with mock.patch("uuid.uuid4", lambda: deduplication_id):
            message_id = publisher.publish(topic, message, group)

        self.assertEqual(message_id, response["MessageId"])
        self.client.publish.assert_called_once_with(
            TargetArn=topic,
            Message=message,
            MessageGroupId=group,
            MessageDeduplicationId=str(deduplication_id),
        )
