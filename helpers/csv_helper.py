import csv


def list_to_csv_file(
    data_list: list, csv_file_path: str, header_names: list[str] = None
):

    if data_list is not None or data_list.__len__() > 0:

        data_list_type = type(data_list[0])

        if data_list_type is not dict:
            data_dict_list = list(map(vars, data_list))
            try:
                header_names: list[str] = header_names or data_list[0].__keys__()
            except Exception as e:
                header_names: list[str] = header_names or get_all_keys(data_dict_list)
        else:
            data_dict_list = data_list
            header_names: list[str] = header_names or (get_all_keys(data_dict_list))

        # Write the list of Person objects to the CSV file
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header_names)

            # Write header
            writer.writeheader()

            # Write rows
            # writer.writerows(data_dict_list)

            for data in data_dict_list:
                writer.writerow(data)
    else:
        print("No data to write to CSV file.")


def get_all_keys(data_list: list):
    # Initialize an empty set to collect keys
    all_keys = set()

    # Iterate over each dictionary in the list
    for dictionary in data_list:
        # Update the set of keys with the keys from the current dictionary
        all_keys.update(dictionary.keys())

    # Convert the set of keys to a list
    all_keys_list = list(all_keys)

    return all_keys_list


def csv_file_to_list(file_path: str):

    with open(file_path, "r", encoding="utf8") as read_obj:
        # Return a reader object which will
        # iterate over lines in the given csvfile
        csv_reader = csv.reader(read_obj)

        # convert string to list
        list_of_rows = list(csv_reader)

        keys = list_of_rows[0]

        # Initialize an empty list to store dictionaries
        result = []

        # Iterate over the remaining lists and create dictionaries
        for row in list_of_rows[1:]:
            # Create a dictionary by zipping keys and values
            person_dict = dict(zip(keys, row))
            result.append(person_dict)

        return result
