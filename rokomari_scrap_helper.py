from helpers import json_helper
from helpers import scraping_helper
from models.book_category import BookCategory

base_url: str = 'https://www.rokomari.com'
category_url = 'book/categories'

book_categories_json_file_path = 'book_categories.json'
books_json_file_path: str = 'books.json'


def get_book_categories_url_list() -> list[BookCategory]:
    url = f'{base_url}/{category_url}'
    response = scraping_helper.get_http_response(url)

    if response.status_code != 200:
        return []

    # Parse the HTML content of the page
    soup = scraping_helper.parse_html_content_as_string(response.text)

    div_with_class_name = scraping_helper.find_all_by_class_name(soup, 'div', 'pFIrstCatCaroItem')

    if div_with_class_name:
        a_tags = scraping_helper.find_all_by_tag_name(div_with_class_name, 'a')
        category_raw_list = scraping_helper.get_value_of_attributes(a_tags, 'href')
        category_list = get_value_of_attributes(category_raw_list)
        return category_list
    else:
        return []


def get_book_category_list():
    book_category_json_string: str | None = json_helper.read_file_as_string(book_categories_json_file_path)

    if book_category_json_string is None or book_category_json_string == '' or book_category_json_string == '{}' or book_category_json_string == '[]':
        book_category_list = get_book_categories_url_list()
        book_category_json_string = json_helper.data_to_json_string(book_category_list)
        json_helper.save_json_string_into_file(book_category_json_string, book_categories_json_file_path)
    else:
        book_category_list = json_helper.json_string_to_data(book_category_json_string)

    return book_category_list


def get_value_of_attributes(data_list: list[dict]):
    values: list[BookCategory] = []

    for item in data_list:
        name = item.get('tag').text.strip()
        url = f'{base_url}{item.get('value')}'
        values.append(BookCategory(name, url))

    # values: list[BookCategory] = [BookCategory(item.get('tag').text.strip(), f'{base_url}{item.get('value')}') for item in data_list]
    return values
