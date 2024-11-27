import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['http://books.toscrape.com/']

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'books.csv',
        'FEED_EXPORT_ENCODING': 'utf-8',  # Установка кодировки
    }

    def parse(self, response):
        # Извлечение данных о книгах
        for book in response.css('article.product_pod'):
            yield {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('p.price_color::text').get(),
                'availability': book.css('p.availability::text').get(),
                'link': response.urljoin(book.css('h3 a::attr(href)').get()),  # Полный URL
            }

        # Переход к следующей странице
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

