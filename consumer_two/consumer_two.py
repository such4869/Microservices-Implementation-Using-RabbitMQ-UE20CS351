import pika
import pymongo

connection = pika.BlockingConnection(pika.ConnectionParameters('172.20.0.1'))
channel = connection.channel()

channel.exchange_declare(exchange='microservices_exchange',exchange_type='direct')
channel.queue_declare('insert_queue')
channel.queue_bind(exchange='microservices_exchange',queue='insert_queue')
channel.queue_declare(queue='insert_receive')
channel.queue_bind(exchange='microservices_exchange',queue='insert_receive')

client = pymongo.MongoClient("mongodb://database:27017/", username='admin', password='admin')
db = client["mydatabase"]
col = db["students"]


def onReceiveTwo(ch,methods,properties,body):
    query = body.decode().split(',')
    name = query[0]
    srn = query[1]
    age = query[2]
    ins = {
        "name": name,
        "srn": srn,
        "age": age
    }
    try:
        col.insert_one(ins)
        e = f"Consumer two - Inserted {ins} successfully"
    except Exception as e:
        pass
    channel.basic_publish(exchange='microservices_exchange',routing_key='insert_receive', body=e)
    print(e, flush=True)
    channel.basic_ack(delivery_tag=methods.delivery_tag)
    return ins


channel.basic_consume(
    queue='insert_queue',
    on_message_callback=onReceiveTwo
)

channel.start_consuming()