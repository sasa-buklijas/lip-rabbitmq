import sys
import pika
from random import randint

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# make exchange and type to fanout
# here we are not using queue/topics directly, queue is made automatically 
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = sys.argv[1] or randint(1, 10)
channel.basic_publish(exchange='logs',
                        routing_key='', # same if changed 
                        body=str(message))

print(f" [x] Sent {message}")
connection.close()