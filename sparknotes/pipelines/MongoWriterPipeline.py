import pymysql
from sparknotes import settings


class MongoWriterPipeline(object):
    # ==fc== init mongo client
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    # ==fc== write into db article
    def process_item(self, article, spider):
        try:
            self.cursor.execute(
                """insert into articles(
                   url,
                   title,
                   author,
                   pub_date,
                   summary,
                   header,
                   topics,
                   tags, 
                   body, 
                   image_urls, 
                   image_paths)
                  value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                  article['url'],
                  article['title'],
                  article['author'],
                  article['pub_date'],
                  article['summary'],
                  article['header'],
                  article['topics'],
                  article['tags'],
                  article['body'],
                  ' '.join(article['image_urls']),
                  ' '.join(article['image_paths'])
                )
            )
        except Exception as error:
            print(error)
        self.connect.commit()
        return article

    # ==fc== execute and close connection to mongo
    def close_spider(self, spider):
        self.connect.close()
