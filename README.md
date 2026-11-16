# Books Scraper

Скрипт собирает данные о книгах с учебного сайта [Books to Scrape](https://books.toscrape.com/).

## Запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Запустите сбор данных в Python:
   ```python
   from scraper import scrape_books
   scrape_books(is_save=True)
   ```
   Результат будет сохранён в `books_data.txt`.
3. Запустите тесты:
   ```bash
   pytest tests/test_scraper.py
   ```

## Используемые библиотеки

- requests
- beautifulsoup4
- schedule
- pytest
