from bs4 import BeautifulSoup


def get_posts(html: BeautifulSoup, class_name: str):
    return [
        item.text
        for item in html.find_all(attrs={"class": class_name})
    ]
