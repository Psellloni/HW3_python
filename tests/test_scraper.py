"""Тесты функций парсинга."""

from unittest.mock import Mock, patch

from scraper import get_book_data, scrape_books


BOOK_PAGE = """
<html>
  <h1>Test book</h1>
  <p class="price_color">£10.00</p>
  <p class="star-rating Three"></p>
  <p class="instock availability">\n In stock \n</p>
  <div id="product_description"></div>
  <p>Book description</p>
  <table class="table table-striped">
    <tr><th>UPC</th><td>123</td></tr>
    <tr><th>Number of reviews</th><td>5</td></tr>
  </table>
</html>
"""

CATALOGUE_PAGE = """
<article class="product_pod"><h3>
<a href="book_1/index.html">Book 1</a>
</h3></article>
"""


def test_get_book_data_returns_dictionary():
    response = Mock(text=BOOK_PAGE)
    response.raise_for_status = Mock()

    with patch("scraper.requests.get", return_value=response):
        book = get_book_data("http://example.com/book")

    assert isinstance(book, dict)
    assert book["title"] == "Test book"
    assert book["UPC"] == "123"


def test_get_book_data_reads_rating_and_description():
    response = Mock(text=BOOK_PAGE)
    response.raise_for_status = Mock()

    with patch("scraper.requests.get", return_value=response):
        book = get_book_data("http://example.com/book")

    assert book["rating"] == "Three"
    assert book["description"] == "Book description"


def test_scrape_books_collects_books():
    first_response = Mock(status_code=200, text=CATALOGUE_PAGE)
    first_response.raise_for_status = Mock()
    last_response = Mock(status_code=404)

    with patch(
        "scraper.requests.get", side_effect=[first_response, last_response]
    ):
        with patch("scraper.get_book_data", return_value={"title": "Book 1"}):
            books = scrape_books()

    assert books == [{"title": "Book 1"}]
