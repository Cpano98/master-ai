import pika
import sys

credenciales = pika.PlainCredentials("czthkmld", "1oh50I65aKmnyHQFokVkEnLBOOoGRfBJ")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="shrimp-01.rmq.cloudamqp.com",
    virtual_host="czthkmld",
    credentials=credenciales))
channel = connection.channel()

# Creando los topicos necesarios para la comunicacion entre dispositivos y la raspberry
channel.exchange_declare(exchange='canal', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='canal', queue=queue_name, routing_key="comunicacion")
channel.queue_bind(exchange='canal', queue=queue_name, routing_key="logs")
channel.queue_bind(exchange='canal', queue=queue_name, routing_key="raspberry")


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    resp = 0
    while resp != "exit":
        print("1)Abrir puerta\n2)Cerrar puerta\n3)Prender led\n4)Apagar led\n5)Escribir a otro topico\n6)Leer de otro topico\n7)Salir")
        resp = input("Opcion: ")
        
        match resp:
            case "1":
                print("Abriendo puerta")
                #response = amqp_client.call(1, "puerta")
                channel.basic_publish(exchange='canal', routing_key=f"raspberry", body="1")
                response = 1
                print(f" [.] Got {response}")  
            case "2":
                print("Cerrando puerta")
                #response = amqp_client.call(0, "puerta")
                channel.basic_publish(exchange='canal', routing_key=f"raspberry", body="0")
                response = 1
                print(f" [.] Got {response}")
            case "3":
                print("Encendiendo la luz")
                #response = amqp_client.call(3, "led")
                channel.basic_publish(exchange='canal', routing_key=f"raspberry", body="3")
                response = 1
                print(f" [.] Got {response}")
            case "4":
                print("Apagando la luz")
                #response = amqp_client.call(2, "led")
                channel.basic_publish(exchange='canal', routing_key=f"raspberry", body="2")
                response = 1
                print(f" [.] Got {response}")
            case "5":
                print("Escribiendo a queue")
                q = input("Ingresa el nombre de la ruta: ")
                m = input("Ingresa el cuertpo del mensaje: ")
                
                if q.startswith("com"):
                    channel.basic_publish(exchange='canal', routing_key=f"comunicacion", body=m)
                if q.startswith("logs"):
                    channel.basic_publish(exchange='canal', routing_key="logs", body=m)
                print(f" [x] Sent {q}: {m}")
            # case "6":
            #     q = input("Ingresa el nombre de la ruta: ")
            #     m = input("Ingresa el cuertpo del mensaje: ")

            #     channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            #     channel.start_consuming()

            #     amqp_client.leer_mensaje(q)
            #     response = 1
            case _:
                connection.close()
                resp = "exit"
main()