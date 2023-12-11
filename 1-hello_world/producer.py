import pika
from random import randint

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

rn = randint(1, 1000)
channel.basic_publish(exchange='',
                    routing_key='hello',
                    body=f'Hello World {rn} !')
print(f" [x] Sent 'Hello World {rn} !'")

connection.close()
