import scrapy
from itemloaders.processors import TakeFirst, Join, MapCompose

def strip_quotes(value):
    return value.strip('“”')


class QuoteItem(scrapy.Item):
    text = scrapy.Field(
        input_processor=MapCompose(str.strip, strip_quotes),
        output_processor=TakeFirst()
    )
    author = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    tags = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join(", ")
    )
