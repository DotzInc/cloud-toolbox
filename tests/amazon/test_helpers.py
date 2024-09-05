import unittest

from cloud.amazon import helpers


class TestBuildAttributes(unittest.TestCase):
    def test_build_attributes(self):
        data = {"foo": "bar", "bar": b"baz", "baz": 42}
        expected = {
            "foo": {"StringValue": data["foo"], "DataType": "String"},
            "bar": {"BinaryValue": data["bar"], "DataType": "Binary"},
            "baz": {"StringValue": str(data["baz"]), "DataType": "Number"},
        }
        attributes = helpers.build_attributes(data)

        self.assertEqual(attributes, expected)

    def test_build_attributes_with_invalid_data(self):
        data = {"foo": None}
        error = "^None of type NoneType is not supported$"

        with self.assertRaisesRegex(TypeError, error):
            helpers.build_attributes(data)  # type: ignore
