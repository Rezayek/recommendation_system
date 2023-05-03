import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='new_review_queue')

channel.basic_publish(exchange='', routing_key='new_review_queue', body='''{
        "user_id": 2609,
        "novel_id": 5000,
        "rating": 4
    }''')
print(" [x] Sent msg sended'")
connection.close()