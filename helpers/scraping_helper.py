import requests
from bs4 import BeautifulSoup, ResultSet, NavigableString, Tag


def get_http_response(url: str):
    return requests.get(url, timeout=10)


def find_all_by_class_name(soup: BeautifulSoup, name=None, class_value=None):
    if class_value is None:
        class_value = ""
    return soup.find_all(name, {"class": class_value})


def find_one_by_class_names_from_soup(
    soup: BeautifulSoup, name: str = None, class_value: str = None
):
    if class_value is None:
        class_value = ""
    return soup.find(name, {"class": class_value})


def find_all_by_tag_name(
    result_set: ResultSet, name=None
) -> list[Tag | NavigableString | None]:
    tag_list: list[Tag | NavigableString | None] = [
        item.find(name) for item in result_set
    ]
    return tag_list


def find_one_by_class_name_from_tag(tag: Tag, class_name: str) -> Tag | None:
    result_tag = tag.select_one(f".{class_name}")
    return result_tag


def get_value_of_attributes(
    tag_list: list[Tag | NavigableString | None], attribute_name=None
):
    values: list[dict] = [
        {"tag": tag, "value": tag.get(key=attribute_name)} for tag in tag_list
    ]
    return values


def parse_html_content_as_string(content_str: str, features: str = "html.parser"):
    return BeautifulSoup(content_str, features)
