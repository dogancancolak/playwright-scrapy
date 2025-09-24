import json
from scrapy_redis.spiders import RedisSpider
from quotes_project.items import QuoteItem
import uuid
import logging
import redis
import os


class QuotesRedisQueueSpider(RedisSpider):
    name = "quotes_redis_queue"
    redis_key = "quotes:start_urls"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker_id = str(uuid.uuid4())[:8]

    custom_settings = {
        "ITEM_PIPELINES": {
            "quotes_project.pipelines.NdjsonPipeline": 600,
        }
    }

    def parse(self, response):
        logging.info(f"[{self.worker_id}] Crawling: {response.url}")

        for quote in response.css("div.quote"):
            item = QuoteItem()
            item["text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("span small.author::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield item
        
        
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
