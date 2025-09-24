import psycopg2
import json
import pika
import redis
import os
from dotenv import load_dotenv

load_dotenv()

class JsonArrayPipeline:
    def open_spider(self, spider):
        self.file = open("quotes_stream.json", "w", encoding="utf-8")
        self.file.write("[\n")
        self.first_item = True

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(",\n")
        else:
            self.first_item = False
        line = json.dumps(dict(item), ensure_ascii=False, indent=4)
        self.file.write(line)
        return item
    

class NdjsonPipeline:
    def open_spider(self, spider):
        self.file = open("quotes_lines.jsonl", "w", encoding="utf-8")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.flush()
        return item


class PostgresPipeline:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
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
    

class RabbitMQPipeline:
    def open_spider(self, spider):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv("RABBIT_HOST", "localhost"))
        )
        self.channel = self.connection.channel()
        queue_name = os.getenv("RABBIT_QUEUE", "quotes")
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.queue_name = queue_name

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(dict(item), ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        return item


class RedisPipeline:
    def open_spider(self, spider):
        self.redis_client = redis.StrictRedis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True
        )

    def process_item(self, item, spider):
        self.redis_client.rpush("quotes_items", json.dumps(dict(item), ensure_ascii=False))
        return item
    
    def close_spider(self, spider):
        # redis-py closes connection pool automaticly but we can still add this for clarity
        if self.redis_client:
            self.redis_client.close()
