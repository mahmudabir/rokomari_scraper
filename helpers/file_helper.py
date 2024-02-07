import os


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


def save_string_into_file(string: str, file_path: str):
    # Open a file in write mode
    with open(file_path, "w", encoding="utf8") as file:
        # Write the string to the file
        file.write(string)
