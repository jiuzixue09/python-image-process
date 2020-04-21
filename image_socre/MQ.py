import pika
import json
import datetime
import argparse
from phash import HttpClientTools as http
from io import BytesIO
from image_socre.aesthetics import flickr_score


def get_score(url):
    try:
        byte_array = http.do_get(url)
        if byte_array is None:
            return '-1'
        img = BytesIO(byte_array)
        score = float(flickr_score(img))
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
    exchange = 'direct.neptune.retrieval.aesthetic.exchange'
    routing_key = "direct.neptune.retrieval.aesthetic.callback.key"
    queue_name = "direct.neptune.retrieval.aesthetic.callback.queue"

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
    # channel.exchange_declare(exchange=exchange,
    #                          exchange_type='direct', durable=True)
    #
    # channel.queue_declare(queue=queue_name, durable=True)
    print(message)
    channel.basic_publish(exchange=exchange,
                          properties=pika.BasicProperties(content_type='text'),
                          routing_key=routing_key,
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
        # channel.exchange_declare(exchange='direct.neptune.huang.exchange',
        #                          exchange_type="direct", durable=True)
        # result = channel.queue_declare("direct.neptune.huang.queue", durable=True)
        queue_name = 'direct.neptune.retrieval.aesthetic.queue'
        binding_keys = "direct.neptune.retrieval.aesthetic.key"
        channel.queue_bind(exchange="direct.neptune.retrieval.aesthetic.exchange",
                           queue=queue_name, routing_key=binding_keys)

        channel.basic_qos(prefetch_count=10)
        channel.basic_consume(on_message_callback=callback, queue=queue_name)  # no_ack=True

        print("start consuming.")
        channel.start_consuming()
    except Exception as e:
        print(str(e))
        print('connect failed')


parser = argparse.ArgumentParser()
parser.add_argument('config', nargs='?', default='dev', type=str, help="队列配置, 来自`config.json`文件, 例如: python webserivec_SR.py test")
args = parser.parse_args()
config_load = json.loads(open("config.json").read())
config = config_load[args.config]

if __name__ == '__main__':
    main()
