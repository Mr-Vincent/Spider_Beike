import pymysql
from itemadapter import ItemAdapter
from items import BeikeWuhanItem
from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB


class BeikespiderPipeline:
    def __init__(self):
        self.connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            db=MYSQL_DB,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def process_item(self, item, spider):
        if isinstance(item, BeikeWuhanItem):
            self.insert(item)

        return item

    def insert(self, item):
        cursor = self.connection.cursor()
        keys = item.keys()
        values = tuple(item.values())
        fields = ",".join(keys)
        temp = ",".join(["%s"] * len(keys))
        sql = "INSERT INTO wh_loupan (%s) VALUES (%s)" % (fields, temp)
        cursor.execute(sql, values)
        self.connection.commit()
