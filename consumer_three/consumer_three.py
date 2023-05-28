import pika
import pymongo

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.20.0.1'))
channel = connection.channel()

channel.exchange_declare(exchange='microservices_exchange',exchange_type='direct')

channel.queue_declare(queue='delete_queue')
channel.queue_bind(exchange='microservices_exchange',queue='delete_queue')

channel.queue_declare(queue='delete_receive')
channel.queue_bind(exchange='microservices_exchange',queue='delete_receive')


client = pymongo.MongoClient("mongodb://database:27017/", username='admin', password='admin')

db = client["mydatabase"]
col = db["students"]

def onReceiveThree(ch,methods,properties,body):
    srn = body.decode().split(',')
    col.delete_one({"srn":srn[0]})
    ch.basic_ack(delivery_tag=methods.delivery_tag)
    m = f"Printing from consumer three -deleted record with srn {srn}"
    channel.basic_publish(exchange='microservices_exchange', routing_key='delete_receive',body=m)
    print(m, flush=True)

channel.basic_consume(queue='delete_queue',on_message_callback=onReceiveThree)

channel.start_consuming()

