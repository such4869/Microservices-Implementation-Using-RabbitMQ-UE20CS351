import pika
from flask import Flask 
from flask import request 

# Rabbit MQ

connection = pika.BlockingConnection(pika.ConnectionParameters('172.20.0.1'))
channel = connection.channel()

channel.exchange_declare(exchange='health_exchange',exchange_type='direct')
channel.exchange_declare(exchange='microservices_exchange',exchange_type='direct')

# consumer 1 
channel.queue_declare(queue='health_check')
channel.queue_bind(exchange='health_exchange',queue='health_check')
channel.queue_declare(queue='health_receive')
channel.queue_bind(exchange='health_exchange',queue='health_receive')

# consumer 2
channel.queue_declare(queue='insert_queue')
channel.queue_bind(exchange='microservices_exchange',queue='insert_queue')
channel.queue_declare(queue='insert_receive')
channel.queue_bind(exchange='microservices_exchange',queue='insert_receive')

# consumer 4
channel.queue_declare(queue='retrieve_queue')
channel.queue_bind(exchange='microservices_exchange',queue='retrieve_queue')
channel.queue_declare(queue='retrieve_receive')
channel.queue_bind(exchange='microservices_exchange',queue='retrieve_receive')

# consumer 3
channel.queue_declare(queue='delete_queue')
channel.queue_bind(exchange='microservices_exchange',queue='delete_queue')
channel.queue_declare(queue='delete_receive')
channel.queue_bind(exchange='microservices_exchange',queue='delete_receive')



app = Flask(__name__)

def confirm_received(ch,method,proterties,body):
    print(body, flush=True)

@app.route("/consumer_one", methods=['GET'])
def health_check():
    # print("printing from producer - we working", flush=True)
    q = "Are you ok XD " + request.args.get('message')
    channel.basic_publish(exchange='', routing_key='health_check', body=q)
    method_frame, header_frame, body = channel.basic_get(queue='health_receive',auto_ack=True)
    if (method_frame):
        print(f"This is an older message. Producer had received -> {body} <- from consumer_one", flush=True)
    else :
        print("No previous older message in the queue", flush=True)
    return "RabbitMQ connection is not compromised"

@app.route("/consumer_two", methods=['POST'])
def insert():
    q = request.get_json()
    hesaru = q.get("name")
    srn = q.get("srn")
    age = q.get("age")
    channel.basic_publish(exchange='microservices_exchange', routing_key='insert_queue', body=f'{hesaru},{srn},{age}')
    
    method_frame, header_frame, body = channel.basic_get(queue='insert_receive',auto_ack=True)
    if (method_frame):
        print(f"Producer - Received -> {body} <- from consumer_two", flush=True)
    else :
        print("Did not receive anything from consumer two", flush=True)
    
    return f"Inserted {hesaru},{srn},{age}"

@app.route("/consumer_three",methods=['GET'])
def delete():
    q = request.get_json()
    # print(">>>",q,flush=True)
    srn = q.get("srn")
    channel.basic_publish(exchange='', routing_key='delete_queue', body=srn)
    method_frame, header_frame, body = channel.basic_get(queue='delete_receive',auto_ack=True)
    if (method_frame):
        print(f"Producer - Received -> {body} <- from consumer_three", flush=True)
    else :
        print("Did not receive anything from consumer three", flush=True)
    return f"Deleted record with srn {srn}"

@app.route("/consumer_four",methods=['GET'])
def readdb():
    q = ''
    channel.basic_publish(exchange='', routing_key='retrieve_queue', body=q)
    method_frame, header_frame, body = channel.basic_get(queue='retrieve_receive',auto_ack=True)
    if (method_frame):
        for doc in body.decode():
            print(f"Producer - Received -> {doc} <- from consumer_four", flush=True)
    else :
        print("Did not receive anything from consumer four", flush=True)
    return "Read"

if __name__ == '__main__':
    print("Producer Started")
    app.run(host='0.0.0.0', port=5000, debug=True)  