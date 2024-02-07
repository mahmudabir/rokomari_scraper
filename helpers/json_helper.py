import json


def json_string_to_data(json_string: str):
    data = json.loads(json_string)
    return data


def data_to_json_string(data):
    ensure_ascii_value = False
    indent_value = 4
    data = json.dumps(
        data,
        default=lambda x: x.__dict__,
        ensure_ascii=ensure_ascii_value,
        indent=indent_value,
    )
    return data
