import pika
import sys


credenciales = pika.PlainCredentials("czthkmld", "1oh50I65aKmnyHQFokVkEnLBOOoGRfBJ")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="shrimp-01.rmq.cloudamqp.com",
    virtual_host="czthkmld",
    credentials=credenciales))

channel = connection.channel()

channel.exchange_declare(exchange='canal', exchange_type='topic')


result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue


binding_keys = ["#"]
for binding_key in binding_keys:
    channel.queue_bind(exchange='canal', queue=queue_name, routing_key="comunicacion")
    channel.queue_bind(exchange='canal', queue=queue_name, routing_key="logs")
    channel.queue_bind(exchange='canal', queue=queue_name, routing_key="raspberry")

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")
    #channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()