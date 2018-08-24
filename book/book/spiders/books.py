# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['bookauthority.org']
    start_urls = ['https://bookauthority.org/experts']

    def parse(self, response):
        names = response.xpath('//script/text()').re(r'"username":"(.*?)"')
        if names:
            for name in names:
                yield SplashRequest(
                    response.urljoin('https://bookauthority.org/profile/'+name),
                    self.parse_page,
                    args={
                        'wait': 3.5,
                    }
                )

    @staticmethod
    def parse_page(response):
        item = {}
        asin = response.xpath('//a[@class="book-title"]/@href').re(r'dp/(.*?)\?tag')
        name = response.xpath('//h1[@class="pg-title"]/text()').extract_first()
        bio = response.xpath('//h2[@class="pg-subtitle"]/text()').extract_first()
        item['Link on BookAuthority'] = response.url

        if asin:
            for index, asn in enumerate(asin):
                item['amazon ASIN '+str(index)] = asn
        if name:
            item['Name'] = name
        if bio:
            item['Bio'] = bio

        yield item
