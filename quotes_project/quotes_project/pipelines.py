import psycopg2
import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("quotes_pipeline.json", "w", encoding="utf-8")
        self.file.write("[")
        self.first_item = True

    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(",\n")
        else:
            self.first_item = False
        line = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(line)
        return item


class PostgresPipeline:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host="localhost",
            dbname="scrapydb",
            user="postgres",
            password="postgres"
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute(
            """
            INSERT INTO quotes (text, author, tags)
            VALUES (%s, %s, %s)
            """,
            (item['text'], item['author'], item['tags'])
        )
        self.connection.commit()
        return item