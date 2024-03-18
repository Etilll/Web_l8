import pika

from datetime import datetime
import sys
import connect
import json
from models import Contact
from faker import Faker
from faker.providers import address
from bson import json_util

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')


def main():
    fake = Faker()
    fake.add_provider(address)
    for i in range(5):
        cont = Contact(fullname = fake.name(), email = fake.email(), address = fake.address(), data = fake.text(), received = False).save()
        print(cont.id)
        message = {
            "id": cont.id,
            "text": f"{fake.text()}",
            "date": datetime.now().isoformat()
        }

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json_util.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    connection.close()
    
    
if __name__ == '__main__':
    main()