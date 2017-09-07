from sparknotes.common.ConfigFiles import ConfigFiles
from sparknotes.common.MongoUtils import MongoUtils


class MongoWriterPipeline(object):
    # ==fc== init mongo client
    def __init__(self):
        config = ConfigFiles.config()
        self.client = MongoUtils.create_client_from_config(config)
        self.db = self.client.sparknotes
        self.bulk = self.db.articles.initialize_ordered_bulk_op()

    # ==fc== write into db article
    def process_item(self, article, spider):
        stripped_article = {
            "title": article["title"],
            "url": article["url"],
            "author": article["author"],
            "date": article["date"],
            "summary": article["summary"],
            "header": article["header"],
            "topics": article["topics"],
            "tags": article["tags"],
            "body": article["body"],
        }

        self.bulk.insert(stripped_article)
        return article

    # ==fc== execute and close connection to mongo
    def close_spider(self, spider):
        result = self.bulk.execute()
        print("Article write result:")
        print(result)
        self.client.close()
