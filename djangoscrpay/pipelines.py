# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class SQLlitePipeline(object):
    
    def open_spider(self, spider):
        self.connection = sqlite3.connect("movie.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_movies(
                    title TEXT,
                    critics_consensus TEXT,
                    approval_percentage TEXT,
                    date TEXT,
                    url TEXT
                )
            
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()


    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO best_movies (title,critics_consensus,approval_percentage,date,url) VALUES(?,?,?,?,?)

        ''', (
            item.get('title'),
            item.get('critics_consensus'),
            item.get('approval_percentage'),
            item.get('date'),
            item.get('url')
        ))
        self.connection.commit()
        return item

