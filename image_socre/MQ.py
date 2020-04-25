import pika
import json
import datetime
import argparse

from phash import HttpClientTools as http
from io import BytesIO
from image_socre.aesthetics import Aesthetics

aesthetic = Aesthetics()

EXCHANGE = "direct.neptune.retrieval.aesthetic.exchange"
Q_NAME = "direct.neptune.retrieval.aesthetic.queue"
R_KEY = "direct.neptune.retrieval.aesthetic.key"

# callback
CALLBACK_EXCHANGE = EXCHANGE
CALLBACK_Q_NAME = "direct.neptune.retrieval.aesthetic.callback.queue"
CALLBACK_KEY = "direct.neptune.retrieval.aesthetic.callback.key"


def get_score(url):
    try:
        byte_array = http.do_get(url)
        if byte_array is None:
            return '-1'
        img = BytesIO(byte_array)
        score = float(aesthetic.aesthetic_score(img))
        return score
    except Exception as _:
        return '-1'


def callback(ch, method, properties, body):
    print(str(datetime.datetime.now()), body)
    req = json.loads(body.decode('utf-8'))
    url = req['img_url']
    img_id = req['id']

    score = get_score(url)
    result = json.dumps({'id': img_id, 'score': score}, ensure_ascii=False)
    publish_message(result)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def publish_message(message):
    user_pwd = pika.PlainCredentials(config["username"], config["password"])

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=config["host"],
            port=config["port"],
            virtual_host=config["virtual-host"],
            credentials=user_pwd,
        )
    )

    channel = connection.channel()
    print(message)
    channel.basic_publish(exchange=CALLBACK_EXCHANGE,
                          properties=pika.BasicProperties(content_type='text'),
                          routing_key=CALLBACK_KEY,
                          body=message)
    connection.close()


def main():
    try:
        user_pwd = pika.PlainCredentials(
            config["username"],
            config["password"]
        )

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config["host"],
                port=int(config["port"]),
                virtual_host=config["virtual-host"],
                credentials=user_pwd,
                heartbeat=0
            )
        )

        channel = connection.channel()
        channel.queue_bind(exchange=EXCHANGE, queue=Q_NAME, routing_key=R_KEY)

        channel.basic_qos(prefetch_count=3)
        channel.basic_consume(on_message_callback=callback, queue=Q_NAME)

        print("start consuming.")
        channel.start_consuming()
    except Exception as e:
        print(str(e))
        print('connect failed')


parser = argparse.ArgumentParser()
parser.add_argument('config', nargs='?', default='dev', type=str, help="队列配置, 来自`config.json`文件, 例如: python "
                                                                       "webserivec_SR.py test")
args = parser.parse_args()
config_load = json.loads(open("config.json").read())
config = config_load[args.config]

if __name__ == '__main__':
    main()

# LRU_CACHE_CAPACITY=1
# resolve memory leak bus
