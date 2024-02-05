import math
import pandas

from helpers import json_helper as jh
from helpers import scraping_helper as sh
from models.book_category import BookCategory
from models.book import Book
from bs4 import Tag

base_url: str = "https://www.rokomari.com"
category_page_url = "book/categories"

book_categories_json_file_path = "book_categories.json"
books_json_file_path: str = "books.json"


def get_book_categories_url_list() -> list[BookCategory]:
    url = f"{base_url}/{category_page_url}"
    response = sh.get_http_response(url)

    if response.status_code != 200:
        return []

    # Parse the HTML content of the page
    soup = sh.parse_html_content_as_string(response.text)

    div_with_class_name = sh.find_all_by_class_name(soup, "div", "pFIrstCatCaroItem")

    if div_with_class_name:
        a_tags = sh.find_all_by_tag_name(div_with_class_name, "a")
        category_raw_list = sh.get_value_of_attributes(a_tags, "href")
        category_list = get_value_of_attributes(category_raw_list)
        return category_list
    else:
        return []


def get_book_category_list():
    book_category_json_string: str | None = jh.read_file_as_string(
        book_categories_json_file_path
    )

    if (
        book_category_json_string is None
        or book_category_json_string == ""
        or book_category_json_string == "{}"
        or book_category_json_string == "[]"
    ):
        book_category_list = get_book_categories_url_list()
        book_category_json_string = jh.data_to_json_string(book_category_list)
        jh.save_json_string_into_file(
            book_category_json_string, book_categories_json_file_path
        )
    else:
        book_category_list = jh.json_string_to_data(book_category_json_string)

    return book_category_list


def get_value_of_attributes(data_list: list[dict]):
    values: list[BookCategory] = []

    for item in data_list:
        name = item.get("tag").text.strip()
        url = f"{base_url}{item.get('value')}"
        values.append(BookCategory(name, url))

    # values: list[BookCategory] = [BookCategory(item.get('tag').text.strip(), f'{base_url}{item.get('value')}') for item in data_list]
    return values


def get_book_categories_containing_url_segment(
    book_category_list: list[BookCategory], url_segment: str
):
    items = book_category_list

    # urls_with_str = [item['url']
    #                     for item in items if url_segment in item['url']]
    # print(urls_with_str)

    df = pandas.DataFrame(items)
    filtered_data = df[df["url"].str.contains(url_segment)]
    filtered_rows = filtered_data.iterrows()
    urls_with_str = [
        BookCategory(row["name"], row["url"]) for index, row in filtered_rows
    ]

    # print(urls_with_str)

    return urls_with_str


def get_book_categories_not_containing_url_segment(
    book_category_list: list[BookCategory], url_segment: str
):
    items = book_category_list

    # urls_without_str = [item['url']
    #                  for item in items if url_segment not in item['url']]
    # print(urls_without_str)

    df = pandas.DataFrame(items)
    filtered_data = df[~df["url"].str.contains(url_segment)]
    filtered_rows = filtered_data.iterrows()
    urls_without_str = [
        BookCategory(row["name"], row["url"]) for index, row in filtered_rows
    ]

    # print(urls_without_str)

    return urls_without_str


def generate_book_object_from_tag(book_card_item: Tag) -> Book:
    # book_url
    tag_item = sh.find_all_by_tag_name(book_card_item, "a")[1]
    all_book_urls = sh.get_value_of_attributes([tag_item], "href")
    book_url = base_url + all_book_urls[0].get("value").strip()

    # image_url
    book_image_item = sh.find_all_by_tag_name(book_card_item, "img")[1]
    all_image_urls = sh.get_value_of_attributes([book_image_item], "src")
    image_url = base_url + all_image_urls[0].get("value").strip()

    # book-title
    book_title_item = sh.find_one_by_class_names_from_soup(
        book_card_item, "h4", "book-title"
    )
    book_title = book_title_item.text.strip()

    # book-author
    book_author_item = sh.find_one_by_class_names_from_soup(
        book_card_item, "p", "book-author"
    )
    book_author = book_author_item.text.strip()

    # book-status text-capitalize
    book_available_item = sh.find_one_by_class_names_from_soup(
        book_card_item, "p", "book-status text-capitalize"
    )
    is_book_available = (
        book_available_item.text.strip().upper() == "Product in stock".upper()
    )

    # book-price
    has_discount = False
    book_original_price = 0
    book_current_price = 0

    if book_card_item.text.strip().upper().count("TK.") == 1:
        has_discount = True

        try:
            # original-price pl-2
            book_original_price_item = sh.find_one_by_class_names_from_soup(
                book_card_item, "strike", "original-price pl-2"
            )
            book_original_price_text = book_original_price_item.text.strip().split()[1]

            book_original_price = (float)(book_original_price_text.replace(",", ""))
            book_current_price = book_original_price
        except Exception as ex:
            book_original_price = 0

        try:
            book_price_tag = sh.find_one_by_class_name_from_tag(
                book_card_item, "book-price"
            )
            book_current_price_text = book_price_tag.contents[-1].text.strip()

            book_current_price = (float)(
                book_current_price_text.split()[-1].replace(",", "")
            )
        except Exception as ex:
            book_current_price = 0

        book_original_price = book_current_price
    else:
        has_discount = False

        try:
            # original-price pl-2
            book_original_price_item = sh.find_one_by_class_names_from_soup(
                book_card_item, "strike", "original-price pl-2"
            )
            book_original_price_text = book_original_price_item.text.strip().split()[1]
            book_original_price = (float)(book_original_price_text.replace(",", ""))
        except Exception as ex:
            book_original_price = 0

        try:
            book_price_tag = sh.find_one_by_class_name_from_tag(
                book_card_item, "book-price"
            )
            book_current_price_text = book_price_tag.contents[-1].text.strip()

            book_current_price = (float)(
                book_current_price_text.split()[-1].replace(",", "")
            )
        except Exception as ex:
            book_current_price = 0

    book = Book(
        title=book_title,
        author=book_author,
        isAvailable=is_book_available,
        originalPrice=book_original_price,
        currentPrice=book_current_price,
        imageUrl=image_url,
        bookUrl=book_url,
        # category=book_category,
    )

    return book


def get_max_page_number(book_category: BookCategory) -> int:
    pagination_response = sh.get_http_response(book_category.url)
    if pagination_response.status_code == 200:
        pagination_soup = sh.parse_html_content_as_string(pagination_response.text)
        pagination_element = sh.find_one_by_class_names_from_soup(
            pagination_soup, "div", "pagination"
        )

        pagination_list = pagination_element.text.strip().split()
        numbers = [int(x) for x in pagination_list if x.isdigit()]
        largest_page_number = max(numbers)
        return largest_page_number
    else:
        return 0


def get_all_books_with_dynamic_category(dynamic_book_category_list: list[BookCategory]):

    book_list: list[Book] = []

    print("\n")
    print("Completed 0.0%", end="\r")

    category_count = dynamic_book_category_list.__len__()

    for i in range(category_count):
        book_category = dynamic_book_category_list[i]
        max_page_number = get_max_page_number(book_category)

        for value in range(max_page_number):

            try:
                list_page_url = f"{book_category.url}&page={value+1}"

                book_list_page_response = sh.get_http_response(list_page_url)

                book_card_list: list[Tag] = []

                if book_list_page_response.status_code == 200:

                    book_list_page_soup = sh.parse_html_content_as_string(
                        book_list_page_response.text
                    )

                    book_card_list: list[Tag] = sh.find_all_by_class_name(
                        book_list_page_soup, "div", "books-wrapper__item"
                    )

                    for book_card_item in book_card_list:

                        try:
                            book = generate_book_object_from_tag(book_card_item)
                            book.category = book_category
                            book_list.append(book)
                        except Exception as ex:
                            print(
                                "Error in: Page ", value + 1, " of ", book_category.name
                            )

            except Exception as ex:
                print("Error in: Page ", value + 1, " of ", book_category.name)

        percentage = round((i / category_count) * 100, 2)
        print(f"Completed {percentage}%", end="\r")

    print("\n")
    return book_list
