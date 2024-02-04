import pandas

from helpers import json_helper as jh
from helpers import scraping_helper as sh
from models.book_category import BookCategory

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
    # urls_with_str: list[BookCategory] = df[df["url"].str.contains(url_segment)][
    #     "name"
    # ].tolist()

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
