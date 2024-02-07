import rokomari_scrap_helper as rsh
from helpers import file_helper as fh
from helpers import json_helper as jh
from models.book_category import BookCategory


def main():

    book_category_list: list[BookCategory] = rsh.get_book_category_list()

    print("Total Book Categories Count: ", book_category_list.__len__())

    dynamic_book_category_list = rsh.get_book_categories_containing_url_segment(
        book_category_list, "/book/category"
    )
    print("Total Dynamic Book Categories Count: ", dynamic_book_category_list.__len__())

    static_book_category_list = rsh.get_book_categories_not_containing_url_segment(
        book_category_list, "/book/category"
    )
    print("Total Static Book Categories Count: ", static_book_category_list.__len__())

    book_list = rsh.get_all_books_with_dynamic_category(dynamic_book_category_list)

    print(f"Books Count: {book_list.__len__()}")
    print(f"Books: \n {jh.data_to_json_string(book_list)}")

    book_list_json_string = jh.data_to_json_string(book_list)
    fh.save_string_into_file(book_list_json_string, rsh.books_json_file_path)
    print(f"Books list saved into {rsh.books_json_file_path} file.")


if __name__ == "__main__":
    print("\n")
    main()

    # try:
    #     print("\nPress any key to continue...")
    #     ch.wait_for_key()
    # except Exception as ex:
    #     pass
