import pika, sys, os
from .data_modifier import add_new_review

# Add the parent directory of the current script (i.e., middleware_listener) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import settings from util.config
from util.config import settings

import keyboard


def launch_review_Listenner():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.HOST))
    channel = connection.channel()

    channel.queue_declare(queue=settings.REVIEW_QUEUE)

    def callback(ch, method, properties, body):

        success = add_new_review(body)

        if success:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=settings.REVIEW_QUEUE,
                          on_message_callback=callback,
                          auto_ack=False)

    print(' [*] review listener:  Waiting for messages.')
    channel.start_consuming()


def run_review_listener():

    try:
        # print("Novel listenner is running. Press Ctrl+Shift+n to stop.")
        # keyboard.add_hotkey('ctrl+shift+s', launch_novel_Listenner)
        launch_review_Listenner()
    except:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

