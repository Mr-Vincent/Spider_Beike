

import scrapy


class BeikeWuhanItem(scrapy.Item):
    name = scrapy.Field()
    lp_type = scrapy.Field()
    image = scrapy.Field()
    block = scrapy.Field()
    address = scrapy.Field()
    room_type = scrapy.Field()
    spec = scrapy.Field()
    ava_price = scrapy.Field()
    total_range = scrapy.Field()
    tags = scrapy.Field()
    detail_url = scrapy.Field()
    create_time = scrapy.Field()

