# Microservice architecture using RabbitMQ

## Cloud Computing
## UE20CS351

### Theory : 
The microservice architecture is one of the most popular forms of deployment, especially in larger organizations where there are multiple components that can be loosely coupled together. Not only does this make it easier to work on separate components independently, but ensures that issues in one component do not bring down the rest of the service. A microservices architecture consists of a collection of small, autonomous services where each service is self-contained and should implement a single business capability within a bounded context. This also comes with the advantage that a single system can scale thereby limiting the resources to required components. For example, during a shopping sale, the cart and payment microservices might need more resources than the login microservice.

RabbitMQ is a message-queueing software also known as a message broker or queue manager. Simply said; it is software where queues are defined, to which applications connect in order to transfer a message or messages.

### What this project will have accomplished
Build and deploy a microservices architecture where multiple components communicate with each other using RabbitMQ. A message broker is an architectural pattern for message validation, transformation and routing. For the scope of this project, we will build 4 microservices: A HTTP server that handles incoming requests to perform CRUD operations on a Student Management Database + Check the health of the RabbitMQ connection, a microservice that acts as the health check endpoint, a microservice that inserts a single student record, a microservice that retrieves student records, a microservice that deletes a student record given the SRN.



### Steps to execute : 

1. To run the files, make sure you have docker installed as well as an image for Rabbit MQ installed through docker. 

2. Run the commands : `docker network create brokernet` followed by `docker run --rm  --network brokernet -it -p 15672:15672 -p 5672:5672 --name rabbitmq -e RABBITMQ_HEARTBEAT=600 rabbitmq`. This will create the docker network called `brokernet`. All of our containers will be attached to this network in order to communicate to each other. 

3. Now that the network is created, we still have to make sure the producers and consumers connect to the correct gateway. This gateway IP address of this network `brokernet` can be found by executing the command : `docker network inspect brokernet`. You will be able to find the gateway IP in the details that are displayed. This IP address must be inserted in the all of the `consumer_..` files and the `producer` file. The exact line of code that needs to be changed is : `connection = pika.BlockingConnection(pika.ConnectionParameters('gateway IP Address'))`. This initialization must be done everytime the docker network is destroyed using the `docker compose down` command.

4. Now that the network has been initialised, open another terminal in the same directory and run 
```
docker compose build
docker compose up
```

5. Then create HTTP requests using Postman to the url `http://localhost:5000/consumer_..` to observe the working of the microservice architecture. 

6. Once you are done, `control + C` in the terminal running the `docker-compose` file and in the rabbit mq network terminal as well. Then type `docker compose down` and press enter. 

### Future works :

- When the producer receives a message from the consumer, sometimes it prints the older message from the queue and not the latest one. This could be due to different execution times.  

- Create a front end interface for the user to create HTTP requests.

