from typing import Mapping, Union

DataType = Union[str, bytes, int, float]
MessageAttributes = Mapping[str, Mapping[str, DataType]]


def build_attributes(data: Mapping[str, DataType]) -> MessageAttributes:
    attrs = {}

    for key, value in data.items():
        if isinstance(value, str):
            attr = {"StringValue": value, "DataType": "String"}
        elif isinstance(value, bytes):
            attr = {"BinaryValue": value, "DataType": "Binary"}
        elif isinstance(value, (int, float)):
            attr = {"StringValue": str(value), "DataType": "Number"}
        else:
            raise TypeError(f"{value} of type {type(value).__name__} is not supported")

        attrs[key] = attr

    return attrs
