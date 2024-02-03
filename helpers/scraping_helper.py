import requests
from bs4 import BeautifulSoup, ResultSet, NavigableString, Tag

from models.book_category import BookCategory


def get_http_response(url: str):
    return requests.get(url, timeout=5)


def find_all_by_class_name(soup: BeautifulSoup, name=None, class_value=None):
    if class_value is None:
        class_value = ''
    return soup.find_all(name, {'class': class_value})


def find_all_by_tag_name(result_set: ResultSet, name=None) -> list[Tag | NavigableString | None]:
    tag_list: list[Tag | NavigableString | None] = [item.find(name) for item in result_set]
    return tag_list


def get_value_of_attributes(tag_list: list[Tag | NavigableString | None], attribute_name=None):
    values: list[BookCategory] = []

    for tag in tag_list:
        name = tag.text.strip()
        url = tag.get(attribute_name)
        values.append(BookCategory(name, url))

    # values = [BookCategory(tag.text.strip(), tag.get(attribute_name)) for tag in tag_list]
    return values


def parse_html_content_as_string(content_str: str, features: str = 'html.parser'):
    return BeautifulSoup(content_str, features)
