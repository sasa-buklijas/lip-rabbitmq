import pika, time


def main():
    rabbitmq_url = 'amqp://guest:guest@localhost:5672/%2f'
    
    params = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel

    # Declare a Stream, named test_stream
        # no error if it already exist
    channel.queue_declare(
        queue='test_stream',
        durable=True,
        #exclusive=True,
        arguments={"x-queue-type": "stream", 
                    'x-max-age': '1M',
                    "x-stream-max-segment-size-bytes": 500,
                    }
    )

    # is around 2 msg, after 3 deleting
    #"x-stream-max-segment-size-bytes": 500,



    # Publish a message to the test_stream
    channel.basic_publish(
        exchange='',
        routing_key='test_stream',
        body=f'Email message from {time.time()}'
    )


if __name__ == '__main__':
    main()
