import pika, os, time


def send_welcome_email(msg):
    #print("Welcome Email task processing")
    print(" [x] Received " + str(msg))
    time.sleep(1) # simulate sending email to a user --delays for 5 seconds
    print("Email successfully sent!")
    return


def main():
    url = 'amqp://guest:guest@localhost:5672/%2f'

    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel

    # Declare our stream
        # even though test_stream is declared from the publishing side, 
        # it's good practice to declare it from the consuming side as well.
    channel.queue_declare(
        queue='test_stream',
        durable=True,
        arguments={"x-queue-type": "stream",
                    'x-max-age': '1M',
                    "x-stream-max-segment-size-bytes": 500,
                    }
    )

    # create a function which is called on incoming messages
    def callback(ch, method, properties, body):
        send_welcome_email(body)

    # Set the consumer QoS prefetch
    channel.basic_qos(
        prefetch_count=100
    )

    # Consume messages published to the stream
    channel.basic_consume(
        'test_stream',
        callback,
        # set from what message to consume
        #arguments={"x-stream-offset": 5000}
        # get all messages from first
        arguments={"x-stream-offset": 'first',},
        # get all messages from last(including) messages
        #arguments={"x-stream-offset": "last"}
    )

    # start consuming (blocks)
    channel.start_consuming()
    connection.close()


if __name__ == '__main__':
    main()
