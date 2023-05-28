import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('172.20.0.1'))
channel = connection.channel()
channel.exchange_declare(exchange='health_exchange',exchange_type='direct')
channel.queue_declare(queue='health_check')
channel.queue_declare(queue='health_receive')
channel.queue_bind(exchange='health_exchange',queue='health_receive')
channel.queue_bind(exchange='health_exchange',queue='health_check')



def onReceiveOne(ch,methods,properties,body):
    m = f"Consumer one - Message = {body.decode()} received from producer."
    print(m, flush=True)
    channel.basic_ack(delivery_tag=methods.delivery_tag)
    channel.basic_publish(exchange='health_exchange',routing_key='health_receive',body=m)
    return 'Health is not compromised'

channel.basic_consume(
    queue='health_check',
    on_message_callback=onReceiveOne,
)

channel.start_consuming()