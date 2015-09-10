import scrapy
import re
from yuedu.items import YueduItem

class YueduSpider(scrapy.spiders.Spider):
    name = "yuedu"
    allowed_domians = ['yuedu.fm']
    start_urls = [
        "http://www.yuedu.fm/article/1/"
    ]
    base_url = "http://www.yuedu.fm"

    def parse(self, response):
        item = YueduItem()
        item['title'] = ''.join(response.xpath(".//*[@id='bd']/div[1]/div[1]/div[1]/div[1]/text()").extract())
        if response.xpath(".//*[@id='bd']/div[1]/div[1]/div[2]/div/p/text()").extract() :
            item['content'] = ''.join(response.xpath(".//*[@id='bd']/div[1]/div[1]/div[2]/div/p/text()").extract())
        else:
            item['content'] = ''.join(response.xpath(".//*[@id='bd']/div[1]/div[1]/div[2]/div/text()").extract())
        item['pic'] = ''.join(response.xpath(".//*[@id='bd']/div[1]/div[1]/div[1]/div[3]/img/@src").extract())
        item['source'] = self.base_url + ''.join(response.xpath("//body/script[7]").re("mp3:\"(.*?)\""))
        item['length'] = ''.join(response.xpath(".//*[@id='bd']/div[1]/div[1]/div[1]/div[2]/em[3]/text()").extract())
        item['index'] = ''.join(re.compile(r'\d+').findall(response.url))

        yield item
        href = response.xpath(".//*[@id='bd']/div[1]/div[2]/span[@class='fr']/a/@href").extract()
        if href :
            href = href[0]
            yield scrapy.Request(self.base_url+href, callback=self.parse)

