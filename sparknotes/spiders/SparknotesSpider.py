import scrapy
import os; print(os.getcwd())
from scrapy.spiders import CrawlSpider
from sparknotes.items import SparkItem
from sparknotes.util.stringutil import StringUtil
from sparknotes.util.xpathutil import XpathUtil
from sparknotes.common.ConfigFiles import ConfigFiles

class SparknotesSpider(CrawlSpider):
    name = "sparknotes"
    config = ConfigFiles.config()
    start_urls = [config.get("scrapeUrl")]

    def parse(self, response):
        categories = response.xpath("//" + XpathUtil.xpath_for_class('media-text previewWithImage'))
        for cats in categories:
            item = SparkItem()
            # get title, url, author, date, summary, header from within class (media-text previewWithImage)
            item['title'] = ''.join(StringUtil.get_first(cats.xpath('.//div[1]/h5[1]/a/text()').extract(), ""))
            item['url'] = ''.join(cats.xpath('.//div[2]/a[last()]/@href').extract())
            item['author'] = ''.join(cats.xpath('.//h6/a/text()').extract())
            item['date'] = ''.join(cats.xpath('.//h6/span/text()').extract())
            item['summary'] = ''.join(cats.xpath('.//div[2]/text()').extract() + cats.xpath('.//div[2]/descendant::*/text()').extract())
            item['header'] = ''.join(cats.xpath('.//h4/a/text()').extract())
            #request url from item url and parse the more detailed content

            url = ''.join(item['url'])

            yield scrapy.Request(url, callback=self.parse_dir_contents, meta=item)

        # go to the next page, call back should be parse itself
        next_page_url = response.xpath("//" + XpathUtil.xpath_for_class('load-more')+'/@href').extract_first()

        if next_page_url is not None:
            index = next_page_url.split("/")[-1]
            if int(index)<10:
                next_page_url = response.urljoin(next_page_url)
                yield scrapy.Request(response.urljoin(next_page_url))







    """
    parse the content in pages like this: http://www.bbc.com/news/world-australia-41104634
    """
    def parse_dir_contents(self, response):
        # ==fc== need to get topics/tag/body if any
        item = response.meta
        item['topics'] = response.xpath(".//article/descendant::h6[1]/a/text()").extract()
        item['topics'] = ','.join(item['topics']);
        item['tags'] = response.xpath('.//article/descendant::h6[2]/a/text()').extract()
        item['tags'] = ','.join(item['tags']);
        item['body'] = response.xpath(".//" + XpathUtil.xpath_for_class('copy') + '/descendant::*/text()').extract()
        slidebody = response.xpath('//*[@id="slideText"]/p/text()').extract()
        item['body'] = ''.join(item['body'])+''.join(slidebody)
        yield item

