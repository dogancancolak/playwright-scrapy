import scrapy
from quotes_project.items import QuoteItem

class QuotesJsonSpider(scrapy.Spider):
    name = "quotes_json"
    start_urls = ["http://quotes.toscrape.com"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "quotes_project.pipelines.JsonWriterPipeline": 100,
        }
    }

    def parse(self, response):
        for quote in response.css("div.quote"):
            item = QuoteItem()
            item["text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("span small.author::text").get()
