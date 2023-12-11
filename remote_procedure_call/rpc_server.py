import pika
import time

def fib(n):
    # simulate long processing
    print(f"    fib({n}) calculating START")
    time.sleep(n)  
    print(f"    fib({n}) calculating END")

    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    #print(f'{ch=} {method=} {props=} {body=}')
    n = int(body)

    print(f" [.] fib({n}) calculating START")
    response = fib(n)
    print(f" [.] fib({n}) calculating END")

    ch.basic_publish(exchange='',
                    # queue to replay
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id=props.correlation_id),
                    body=str(response))
    # ack received message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='rpc_queue')

    # takle one by one
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
    
    # exclusive=True there can be onl one connection to it
    # channel.basic_consume(queue='rpc_queue', on_message_callback=on_request, exclusive=True)

    print(" [x] Awaiting RPC requests")

    channel.start_consuming()


if __name__ == '__main__':
    main()
