import time

import rokomari_scrap_helper as rsh
from helpers import common_helper as ch
from helpers import json_helper as jh
from models.book_category import BookCategory


def main():
    start_time = time.time_ns()
    book_category_list: list[BookCategory] = rsh.get_book_category_list()
    end_time = time.time_ns()

    print(jh.data_to_json_string(book_category_list))
    print((end_time - start_time), " ns")
    
    rsh.get_book_categories_containing_url_segment(book_category_list, "/book/category")
    rsh.get_book_categories_not_containing_url_segment(book_category_list, "/book/category")


if __name__ == "__main__":
    main()

    try:
        print("\nPress any key to continue...")
        ch.wait_for_key()
    except Exception as ex:
        pass
