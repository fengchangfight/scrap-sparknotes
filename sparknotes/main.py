from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from sparknotes.spiders.SparknotesSpider import SparknotesSpider

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner(get_project_settings())
d = runner.crawl(SparknotesSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()