import json
import os.path


def save_json_string_into_file(json_string: str, file_path: str):
    # Open a file in write mode
    with open(file_path, "w", encoding="utf8") as file:
        # Write the JSON string to the file
        file.write(json_string)


def read_file_as_string(file_path: str):
    # Check if the file exists in the current directory
    file_exists = os.path.isfile(file_path)

    if not file_exists:
        return None

    try:
        # Open the file in read mode
        with open(file_path, "r", encoding="utf8") as file:
            # Read the file as a string
            content = file.read()
        return content
    except Exception as ex:
        return None


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
