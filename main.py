import rokomari_scrap_helper
from helpers import json_helper, common_helper
from models.book_category import BookCategory


def main():
    book_category_list: list[BookCategory] = rokomari_scrap_helper.get_book_category_list()

    print(json_helper.data_to_json_string(book_category_list))


if __name__ == "__main__":
    main()

    try:
        print('\nPress any key to continue...')
        common_helper.wait_for_key()
    except Exception as ex:
        pass
