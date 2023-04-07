# SENG 468 A2 - Social Media Platform

## Description

Assignment #2 for SENG 468 at the University of Victoria. 

Assignment description:

```
You have been tasked with designing a scalable and fault-tolerant social media platform that allows
users to create and share posts. The platform should support real-time notifications and messaging.
implement this platform.
```
## Components
### Flask Backend
The Flask backend is a simple social media platform that allows users to create accounts, make posts, 
comment on posts, and like posts. It also provides an endpoint to generate user activity reports. 
The app uses MongoDB for data storage and Redis for caching, which helps improve performance. 
Additionally, it utilizes RabbitMQ for sending notifications when a user's post is liked or commented on.

### Redis Cache
Redis is used in this Flask app as a caching mechanism to improve performance. When a user, post, or comment is 
requested, the app first checks if the data is available in the Redis cache. If the data is found in the cache, 
it is returned immediately, reducing the need for database queries. If the data is not found in the cache, 
the app retrieves the data from the MongoDB database, stores it in the cache for future requests, and then returns 
the data to the user. This approach reduces the number of direct database requests, which leads to faster response 
times and improved overall performance.

### NGINX Load Balancer
Nginx is used as a load balancer for the backend Flask app instances. It listens on port 80 for incoming HTTP requests and forwards them to the available Flask app instances, flask_app1 and flask_app2. Nginx uses the least_conn load balancing method, which directs new connections to the backend server with the least number of active connections, ensuring an even distribution of requests.

### MongoDB Database
MongoDB is used as the primary database to store and manage data entities, including users, posts, comments, likes, and notifications. The Flask app communicates with MongoDB to perform CRUD (Create, Read, Update, and Delete) operations on these entities. For instance, when a user creates a post or comments on an existing post, the app stores this information in MongoDB. Note that logs from MongoDB have been muted in the docker-compose file.

### Demo Script Container
The demo script container is used to run the demo script, which simulates user activity on the social media platform. The demo script creates a number of users, posts, comments, and likes, and then generates a user activity report. 
The script populates the database with sample data for testing and generate sample reports
on user activity and performs basic CRUD operations on the database, including creating, reading,
updating, and deleting records

### RabbitMQ Message Broker
RabbitMQ is used as a message broker to send notifications to users when their posts are liked or commented on. When a user likes or comments on a post, the Flask app sends a message to RabbitMQ, which then forwards the message to the appropriate user. The user then receives a notification that their post has been liked or commented on.

### User Servers
The user servers are used to simulate users interacting with the social media platform. Each user server is an app that simulates a user's activity on the social media platform. The user server creates a user account, makes a post, and then likes and comments on other users' posts. The user server subscribes to RabbitMQ and receives notification if another user likes or comments on their post.

## Getting Started

run `docker-compose build` and `docker-compose up` to start the application

## A Highlight of the Logs to Look For
```angular2html
rabbitmq             | 2023-04-07 18:17:54.882476+00:00 [notice] <0.230.0> Logging: configured log handlers are now ACTIVE
redis-noah           | 1:M 07 Apr 2023 18:17:54.986 * DB saved on disk
rabbitmq             | 2023-04-07 18:17:55.613158+00:00 [info] <0.230.0> ra: starting system quorum_queues
rabbitmq             | 2023-04-07 18:17:55.613353+00:00 [info] <0.230.0> starting Ra system: quorum_queues in directory: /var/lib/rabbitmq/mnesia/rabbit@75fa9f811243/quorum/rabbit@75fa9f811243
flask_app1           | 172.29.0.5 - - [07/Apr/2023 18:17:55] "POST /user HTTP/1.0" 201 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:55 +0000] "POST /user HTTP/1.1" 201 28 "-" "python-requests/2.28.2"
flask_app2           | 172.29.0.5 - - [07/Apr/2023 18:17:55] "GET /user/johndoe HTTP/1.0" 200 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:55 +0000] "GET /user/johndoe HTTP/1.1" 200 169 "-" "python-requests/2.28.2"
flask_app1           | 172.29.0.5 - - [07/Apr/2023 18:17:55] "POST /post HTTP/1.0" 201 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:55 +0000] "POST /post HTTP/1.1" 201 44 "-" "python-requests/2.28.2"
rabbitmq             | 2023-04-07 18:17:55.824585+00:00 [info] <0.266.0> ra system 'quorum_queues' running pre init for 0 registered servers
flask_app2           | 172.29.0.5 - - [07/Apr/2023 18:17:55] "GET /post/Hello%20World HTTP/1.0" 200 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:55 +0000] "GET /post/Hello%20World HTTP/1.1" 200 175 "-" "python-requests/2.28.2"
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:55 +0000] "POST /comment HTTP/1.1" 201 47 "-" "python-requests/2.28.2"
flask_app1           | 172.29.0.5 - - [07/Apr/2023 18:17:55] "POST /comment HTTP/1.0" 201 -
flask_app2           | 172.29.0.5 - - [07/Apr/2023 18:17:55] "GET /comment?post_title=Hello+World&author=johndoe HTTP/1.0" 200 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:55 +0000] "GET /comment?post_title=Hello+World&author=johndoe HTTP/1.1" 200 119 "-" "python-requests/2.28.2"
rabbitmq             | 2023-04-07 18:17:55.861245+00:00 [info] <0.267.0> ra: meta data store initialised for system quorum_queues. 0 record(s) recovered
flask_app1           | 172.29.0.5 - - [07/Apr/2023 18:17:55] "POST /like HTTP/1.0" 201 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:55 +0000] "POST /like HTTP/1.1" 201 44 "-" "python-requests/2.28.2"
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:56 +0000] "GET /report/johndoe HTTP/1.1" 200 142 "-" "python-requests/2.28.2"
flask_app2           | 172.29.0.5 - - [07/Apr/2023 18:17:56] "GET /report/johndoe HTTP/1.0" 200 -
flask_app1           | 172.29.0.5 - - [07/Apr/2023 18:17:56] "DELETE /post HTTP/1.0" 200 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:56 +0000] "DELETE /post HTTP/1.1" 200 25 "-" "python-requests/2.28.2"
flask_app2           | 172.29.0.5 - - [07/Apr/2023 18:17:56] "DELETE /user/johndoe HTTP/1.0" 200 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:17:56 +0000] "DELETE /user/johndoe HTTP/1.1" 200 25 "-" "python-requests/2.28.2"
demo                 | STARTING DEMO 1
demo                 | Creating user: alice123
demo                 | Creating user: bob123
demo                 | Creating post: Hello, World!
demo                 | Creating notification for user alice123
demo                 | Creating comment for post Hello, World! by bob123
demo                 | Creating like by bob123 for post Hello, World!
demo                 | Creating notification for user alice123
demo                 | Generating user activity report for alice123
demo                 | {'user_id': 'alice123', 'username': 'alice123', 'posts_created': 1, 'comments_created': 0, 'likes_given': 0, 'likes_received': 1}
demo                 | Generating user activity report for bob123
demo                 | {'user_id': 'bob123', 'username': 'bob123', 'posts_created': 0, 'comments_created': 1, 'likes_given': 1, 'likes_received': 0}
demo                 | DEMO 1 COMPLETE
demo                 |
demo                 |
demo                 | STARTING DEMO 2
demo                 | Creating user: johndoe
demo                 | Created user: johndoe
demo                 | Getting user: johndoe
demo                 | User found in cache: johndoe
demo                 | Retrieved user: {'name': 'John Doe', 'username': 'johndoe', 'email': 'johndoe@example.com', 'password': 'password123', 'date_of_birth': '1990-01-01', 'friends': []}
demo                 | Creating post: My first post
demo                 | Created post with ID: 64305e5363d6a2550e30d140
demo                 | Getting post: My first post
demo                 | Post found in cache: My first post
demo                 | Retrieved post: {'title': 'My first post', 'content': 'This is the content of my first post', 'author': 'johndoe', 'date_of_creation': '2023-04-07 18:17:55.125880', 'likes': 0, 'comments': []}
demo                 | Creating notification for user johndoe
demo                 | Creating comment for post My first post by johndoe
demo                 | Created comment with ID: 64305e5363d6a2550e30d142
demo                 | Getting comment for post My first post by johndoe
demo                 | Comment found in cache: post My first post, author johndoe
demo                 | Retrieved comment: {'content': 'Great post!', 'author': 'johndoe', 'date_of_creation': '2023-04-07 18:17:55.128868', 'likes': 0}
demo                 | Creating notification for user johndoe
demo                 | Created notification with ID: 64305e5363d6a2550e30d143
demo                 | Creating like by johndoe for post My first post
demo                 | Creating notification for user johndoe
demo                 | Created like with ID: 64305e5363d6a2550e30d145
demo                 | Generating user activity report for johndoe
demo                 | User activity report: {'user_id': 'johndoe', 'username': 'johndoe', 'posts_created': 1, 'comments_created': 1, 'likes_given': 1, 'likes_received': 1}
demo                 | Deleting post: My first post
demo                 | Deleted 1 posts
demo                 | Deleting user: johndoe
demo                 | Deleted 1 users
demo                 | DEMO 2 COMPLETE
demo                 |
demo                 |
demo                 | STARTING FLASK DEMO
demo                 | Create user response: {'username': 'johndoe'}
demo                 | Get user response: {'date_of_birth': '1990-01-01 00:00:00', 'email': 'john@example.com', 'friends': [], 'name': 'John Doe', 'password': 'password123', 'username': 'johndoe'}
demo                 | Create post response: {'post_id': '64305e5328bdaf5748d7339f'}
demo                 | Get post response: {'author': 'johndoe', 'comments': [], 'content': 'This is my first post!', 'date_of_creation': '2023-04-07 18:17:55.815077', 'likes': 0, 'title': 'Hello World'}
demo                 | Create comment response: {'comment_id': '64305e5328bdaf5748d733a1'}
demo                 | Get comment response: {'author': 'johndoe', 'content': 'Nice post!', 'date_of_creation': '2023-04-07 18:17:55.832154', 'likes': 0}
demo                 | Create like response: {'like_id': '64305e5328bdaf5748d733a3'}
demo                 | Generate user activity report response: {'comments_created': 2, 'likes_given': 2, 'likes_received': 2, 'posts_created': 1, 'user_id': 'johndoe', 'username': 'johndoe'}
demo                 | Delete post response: {'deleted_count': 1}
demo                 | Delete user response: {'deleted_count': 1}
demo                 | FLASK DEMO COMPLETE
demo exited with code 0

rabbitmq             | 2023-04-07 18:18:10.057504+00:00 [info] <0.864.0> accepting AMQP connection <0.864.0> (172.29.0.8:54456 -> 172.29.0.7:5672)
flask_app1           | 172.29.0.5 - - [07/Apr/2023 18:18:10] "POST /user HTTP/1.0" 201 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:18:10 +0000] "POST /user HTTP/1.1" 201 26 "-" "python-requests/2.28.2"
rabbitmq             | 2023-04-07 18:18:10.063151+00:00 [info] <0.864.0> connection <0.864.0> (172.29.0.8:54456 -> 172.29.0.7:5672): user 'guest' authenticated and granted access to vhost '/'
flask_app2           | 172.29.0.5 - - [07/Apr/2023 18:18:10] "POST /post HTTP/1.0" 201 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:18:10 +0000] "POST /post HTTP/1.1" 201 44 "-" "python-requests/2.28.2"
rabbitmq             | 2023-04-07 18:18:25.010290+00:00 [info] <0.888.0> accepting AMQP connection <0.888.0> (172.29.0.2:36920 -> 172.29.0.7:5672)
rabbitmq             | 2023-04-07 18:18:25.013860+00:00 [info] <0.888.0> connection <0.888.0> (172.29.0.2:36920 -> 172.29.0.7:5672): user 'guest' authenticated and granted access to vhost '/'
rabbitmq             | 2023-04-07 18:18:25.016772+00:00 [info] <0.888.0> closing AMQP connection <0.888.0> (172.29.0.2:36920 -> 172.29.0.7:5672, vhost: '/', user: 'guest')
flask_app1           | 172.29.0.5 - - [07/Apr/2023 18:18:25] "POST /like HTTP/1.0" 201 -
nginx_load_balancer  | 172.29.0.9 - - [07/Apr/2023:18:18:25 +0000] "POST /like HTTP/1.1" 201 44 "-" "python-requests/2.28.2"
user2                | Create user response: {'username': 'user2'}
user2                | Create post response: {'post_id': '64305e61f0c36dc54df4fbda'}
user2                | Sleeping for 15 seconds...
user2                | Listening for notifications for user user2
user2                | Create like response: {'like_id': '64305e7128bdaf5748d733a7'}
rabbitmq             | 2023-04-07 18:18:25.096769+00:00 [info] <0.905.0> accepting AMQP connection <0.905.0> (172.29.0.3:38752 -> 172.29.0.7:5672)
rabbitmq             | 2023-04-07 18:18:25.099795+00:00 [info] <0.905.0> connection <0.905.0> (172.29.0.3:38752 -> 172.29.0.7:5672): user 'guest' authenticated and granted access to vhost '/'
rabbitmq             | 2023-04-07 18:18:25.104148+00:00 [info] <0.905.0> closing AMQP connection <0.905.0> (172.29.0.3:38752 -> 172.29.0.7:5672, vhost: '/', user: 'guest')
flask_app2           | 172.29.0.5 - - [07/Apr/2023 18:18:25] "POST /comment HTTP/1.0" 201 -
nginx_load_balancer  | 172.29.0.8 - - [07/Apr/2023:18:18:25 +0000] "POST /comment HTTP/1.1" 201 47 "-" "python-requests/2.28.2"
user1                | Create post response: {'post_id': '64305e62f0c36dc54df4fbdb'}
user1                | Sleeping for 15 seconds...
user1                | Listening for notifications for user user1
user1                | Received notification: b'notification_type: like, title: User 1 Post'
user1                | Create comment response: {'comment_id': '64305e71f0c36dc54df4fbdd'}

```

