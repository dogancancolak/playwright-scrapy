import scrapy
from quotes_project.items import QuoteItem


class QuotesPlaywrightSpider(scrapy.Spider):
    name = "quotes_playwright"
    start_urls = ["http://quotes.toscrape.com/js/"]
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "ITEM_PIPELINES": {
            "quotes_project.pipelines.NdjsonPipeline": 600,
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={"playwright": True},  # Playwright ile aç
                callback=self.parse
            )

    def parse(self, response):
        for quote in response.css("div.quote"):
            item = QuoteItem()
            item["text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("span small.author::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield item
