import scrapy
from scrapy.loader import ItemLoader
from quotes_project.items import QuoteItem

class QuotesJsonSpider(scrapy.Spider):
    name = "quotes_json"
    start_urls = ["http://quotes.toscrape.com"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "quotes_project.pipelines.JsonArrayPipeline": 100,
        }
    }

    def parse(self, response):
        for quote in response.css("div.quote"):
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_css("text", "span.text::text")
            loader.add_css("author", "span small.author::text")
            loader.add_css("tags", "div.tags a.tag::text")
            yield loader.load_item()

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
