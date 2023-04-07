import os
import time
import requests
import pika
import threading


username1 = "user1"
base_url = "http://nginx:80"


def listen_notifications(username):
    rabbitmq_host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    channel = connection.channel()

    channel.queue_declare(queue=username)

    def callback(ch, method, properties, body):
        print(f"Received notification: {body}")

    channel.basic_consume(queue=username, on_message_callback=callback, auto_ack=True)

    print(f"Listening for notifications for user {username}")
    channel.start_consuming()


if __name__ == "__main__":
    notification_thread = threading.Thread(target=listen_notifications, args=(username1,))
    notification_thread.start()

    # Create user
    data = {
        "name": "User 1",
        "username": username1,
        "email": "john@example.com",
        "password": "password123",
        "date_of_birth": "1990-01-01"
    }
    response = requests.post(f"{base_url}/user", json=data)
    print("Create user response:", response.json())

    # Create post
    data = {
        "title": "User 1 Post",
        "content": "This is my first post!",
        "author": username1
    }
    response = requests.post(f"{base_url}/post", json=data)
    print("Create post response:", response.json())

    print("Sleeping for 15 seconds...")
    time.sleep(15)

    # Create comment
    data = {
        "post_title": "User 2 Post",
        "content": "Nice post!",
        "author": username1
    }
    response = requests.post(f"{base_url}/comment", json=data)
    print("Create comment response:", response.json())
