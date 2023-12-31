import pika
import uuid
import sys

class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        # if I start client first and there is no rpc_queue, make it
        self.connection.channel().queue_declare(queue='rpc_queue')

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        # this is where response will come
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
        else:
            print(f'{self.corr_id=} != {props.correlation_id=}')

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # send for calculation
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        # we will wait until we get response
        self.connection.process_data_events(time_limit=None)
        #print(f'{self.response=}')

        return int(self.response)


def main():
    fibonacci_rpc = FibonacciRpcClient()

    n = sys.argv[1] if len(sys.argv) > 1 else 3

    print(f" [x] Requesting fib({n})")
    response = fibonacci_rpc.call(n)
    print(f" [.] Got {response}")


if __name__ == '__main__':
    main()
