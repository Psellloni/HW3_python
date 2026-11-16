"""Сбор данных о книгах с сайта Books to Scrape."""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_book_data(book_url):
    """Возвращает данные об одной книге по ссылке book_url."""
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    book = {}
    book["title"] = soup.find("h1").text
    book["price"] = soup.find("p", class_="price_color").text

    rating = soup.find("p", class_="star-rating")
    book["rating"] = rating["class"][1]

    availability = soup.find("p", class_="instock availability")
    book["availability"] = availability.text.strip()

    description_header = soup.find(id="product_description")
    if description_header is None:
        book["description"] = ""
    else:
        book["description"] = description_header.find_next_sibling("p").text

    table = soup.find("table", class_="table table-striped")
    for row in table.find_all("tr"):
        key = row.find("th").text
        value = row.find("td").text
        book[key] = value

    return book


def scrape_books(is_save=False):
    """Собирает данные обо всех книгах и при is_save сохраняет их в файл."""
    books = []
    page_number = 1

    while True:
        page_url = (
            "http://books.toscrape.com/catalogue/page-"
            + str(page_number)
            + ".html"
        )
        response = requests.get(page_url)

        if response.status_code == 404:
            break

        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        for article in articles:
            link = article.find("h3").find("a")["href"]
            book_url = urljoin(page_url, link)
            books.append(get_book_data(book_url))

        page_number += 1

    if is_save:
        with open("books_data.txt", "w", encoding="utf-8") as file:
            for book in books:
                file.write(str(book) + "\n")

    return books
