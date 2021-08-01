import json
import datetime
from scrapy import Request, Spider
from items import BeikeWuhanItem
import random
import re

p_room_type = re.compile('[0-9]+')
p_room_spec = re.compile('[\s\S]*㎡$')

root_url = 'https://wh.fang.ke.com/'
default_schema = 'https:'


class BeikeWuhanSpider(Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.curr_page = 1
        self.url_template = "https://wh.fang.ke.com/loupan/nhs1pg%s"

    name = "beike_wuhan"
    allowed_domains = ["wh.fang.ke.com"]

    def start_requests(self):
        # 武汉楼盘的首页
        baseurl = "https://wh.fang.ke.com/loupan/nhs1pg1"

        UserAgents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36']
        UserAgent = random.choice(UserAgents)

        headers = {'User-Agent': UserAgent}
        yield Request(
            url=baseurl,
            headers=headers,
            callback=self.parse)

    def parse(self, response):
        # next_page = response.xpath('/html/body/div[7]/div[2]/')
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield Request(next_page, callback=self.parse)
        # 每页的数量还不是固定的 有的是10个每页 有的是20个每页
        content = response.xpath('/html/body/div[6]/ul[2]/li')
        for item in content:
            image = item.xpath('./a/img/@src')[0].extract()
            name = item.xpath('./div[1]/div[1]/a/@title')[0].extract()
            detail_url = item.xpath('./div[1]/div[1]/a/@href')[0].extract()
            lp_type = item.xpath('./div[1]/div[1]/span[2]/text()').extract_first()
            address = item.xpath('./div[1]/a[1]/text()')[1].extract()
            block = ''
            if address:
                block = address.split('/')[0]
            room_type_texts = item.xpath('./div[1]/a[2]/span/text()').extract()
            room_types = []
            room_spec = ''
            for room_type_text in room_type_texts:
                if re.match(p_room_type, room_type_text):
                    room_types.append(room_type_text)
                if re.match(p_room_spec, room_type_text):
                    room_spec = room_type_text.split(' ')[1]

            room_type = '/'.join(room_types)
            t = item.xpath('./div[1]/div[3]/span/text()').getall()
            tags = ','.join(t)

            ava_price = item.xpath('./div[1]/div[4]/div[1]/span[1]/text()').extract_first()
            total = item.xpath('./div[1]/div[4]/div[2]/text()').extract_first()
            if not total:
                total = ''

            wuhan_item = BeikeWuhanItem()
            wuhan_item['name'] = name
            wuhan_item['lp_type'] = lp_type
            wuhan_item['image'] = default_schema + image
            wuhan_item['block'] = block
            wuhan_item['address'] = address
            wuhan_item['room_type'] = room_type
            wuhan_item['spec'] = room_spec
            wuhan_item['ava_price'] = ava_price
            wuhan_item['total_range'] = total
            wuhan_item['tags'] = tags
            wuhan_item['detail_url'] = root_url + detail_url
            wuhan_item['create_time'] = datetime.datetime.now()
            yield wuhan_item

        # 楼盘总数  如果为0了 那么说明没有下一页了
        count = response.xpath('/html/body/div[6]/div[2]/span[2]/text()').get()
        print('===================================================================', count)
        if int(count) > 0:
            self.curr_page += 1
        else:
            self.crawler.engine.close_spider(self, '任务完成')
        next_page = self.url_template % self.curr_page
        yield Request(next_page, callback=self.parse)
