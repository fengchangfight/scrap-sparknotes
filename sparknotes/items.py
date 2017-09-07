import scrapy
from scrapy.item import Field


class SparkItem(scrapy.Item):
    title = Field()
    url = Field()
    author = Field()
    date = Field()
    summary = Field()
    header = Field()

    topics = Field()
    tags = Field()
    body = Field()
