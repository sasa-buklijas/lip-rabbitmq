import sys
import pika
from random import randint

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# durable=True is making queue persistent
channel.queue_declare(queue='task_queue', durable=True)

message = sys.argv[1] or randint(1, 10)
channel.basic_publish(exchange='',
                        routing_key='task_queue',
                        body=str(message),
                        properties=pika.BasicProperties(
        # delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE is making message persistent
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

print(f" [x] Sent {message}")
connection.close()