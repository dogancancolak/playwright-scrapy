import scrapy
from quotes_project.items import QuoteItem

class QuotesRabbitSpider(scrapy.Spider):
    name = "quotes_rabbit"
    start_urls = ["http://quotes.toscrape.com"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "quotes_project.pipelines.RabbitMQPipeline": 400,
        }
    }

    def parse(self, response):
        for quote in response.css("div.quote"):
            item = QuoteItem()
            item["text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("span small.author::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
