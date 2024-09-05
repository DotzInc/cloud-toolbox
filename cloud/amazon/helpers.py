from typing import Dict, Union

DataType = Union[str, bytes, int, float]
MessageAttributes = Dict[str, Dict[str, DataType]]


def build_attributes(data: Dict[str, DataType]) -> MessageAttributes:
    attrs = {}

    for key, value in data.items():
        if isinstance(value, str):
            attr = {"StringValue": value, "DataType": "String"}
        elif isinstance(value, bytes):
            attr = {"BinaryValue": value, "DataType": "Binary"}
        elif isinstance(value, (int, float)):
            attr = {"StringValue": value, "DataType": "Number"}
        else:
            raise TypeError(f"{value} of type {type(value).__name__} is not supported")

        attrs[key] = attr

    return attrs
