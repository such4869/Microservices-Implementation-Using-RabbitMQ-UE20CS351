import pika
import pymongo

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.20.0.1'))
channel = connection.channel()

channel.exchange_declare(exchange='microservices_exchange',exchange_type='direct')
channel.queue_declare(queue='retrieve_queue')
channel.queue_bind(exchange='microservices_exchange',queue='retrieve_queue')
channel.queue_declare(queue='retrieve_receive')
channel.queue_bind(exchange='microservices_exchange',queue='retrieve_receive')


client = pymongo.MongoClient("mongodb://database:27017/", username='admin', password='admin')

db = client["mydatabase"]
col = db["students"]

def onReceiveFour(ch,methods,properties,body):
    docs = col.find()
    for doc in docs:
        sdoc = "".join(doc)
        #channel.basic_publish(exchange='microservices_exchange',routing_key='retrieve_receive',body=sdoc)
        print(doc, flush=True)
    ch.basic_ack(delivery_tag=methods.delivery_tag)
    
channel.basic_consume(queue='retrieve_queue',on_message_callback=onReceiveFour)

channel.start_consuming()