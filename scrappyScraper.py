from abc import ABC

import scrapy
from scrapy.crawler import CrawlerProcess


class IGNNewsUpdater(scrapy.Spider, ABC):
    name = "IGN news finder"
    start_urls = ['https://www.ign.com/news']

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response, **kwargs):
        SET_SELECTOR = '.content-item'
        for child in response.css(SET_SELECTOR):
            NAME_SELECTOR = '.item-title::text'
            title = child.css(NAME_SELECTOR).get()
            link = 'https://www.ign.com' + child.css('a::attr(href)').get()
            yield {
                'Latest news Title': title,
                'Link to': link
            }


process = CrawlerProcess(settings={
    'FEED': {
        "items.json": {"format": "json"},
    }
})

process.crawl(IGNNewsUpdater)
process.start()
