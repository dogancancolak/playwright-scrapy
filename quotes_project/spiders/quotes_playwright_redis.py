import scrapy
import json
import logging
import uuid
from scrapy_redis.spiders import RedisSpider
from quotes_project.items import QuoteItem


class QuotesPlaywrightRedisSpider(RedisSpider):
    name = "quotes_playwright_redis"
    redis_key = "quotes:playwright:start_urls"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker_id = str(uuid.uuid4())[:8]

    custom_settings = {
        "ITEM_PIPELINES": {
            "quotes_project.pipelines.NdjsonPipeline": 600,
        }
    }

    def make_request_from_data(self, data):
        """Redis'ten gelen datayı scrapy.Request'e çevirir."""
        try:
            if isinstance(data, bytes):
                data = data.decode("utf-8")  # <-- önemli
            obj = json.loads(data)
            url = obj.get("url")
            meta = obj.get("meta", {})
        except Exception:
            url = data
            meta = {}
        meta["playwright"] = True
        logging.info(f"[{self.worker_id}] Creating Request for {url}")
        return scrapy.Request(url, meta=meta, dont_filter=True, callback=self.parse)

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
            next_url = response.urljoin(next_page)
            data = {"url": next_url, "meta": {"playwright": True}}
            self.server.lpush(self.redis_key, json.dumps(data))
            logging.info(f"[{self.worker_id}] Pushed next page to redis: {next_url}")
