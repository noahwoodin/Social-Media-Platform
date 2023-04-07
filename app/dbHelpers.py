import redis
from pymongo import MongoClient
from datetime import datetime
import json
import os
import pika


mongo_client = MongoClient("mongodb://db-noah:27017")
db = mongo_client["SocialMedia"]
redis_client = redis.StrictRedis(host='redis-noah', port=6379, db=0)


def create_user(name, username, email, password, date_of_birth):
    user = {
        "name": name,
        "username": username,
        "email": email,
        "password": password,
        "date_of_birth": date_of_birth,
        "friends": []
    }
    print(f"Creating user: {username}")
    redis_client.set(f'user:{username}', json.dumps(user, default=str))
    result = db.Users.insert_one(user)
    return username


def delete_user(username):
    print(f"Deleting user: {username}")
    redis_client.delete(f'user:{username}')
    result = db.Users.delete_one({"username": username})
    return result.deleted_count


def get_user(username):
    print(f"Getting user: {username}")
    cached_user = redis_client.get(f'user:{username}')
    if cached_user:
        print(f"User found in cache: {username}")
        return json.loads(cached_user)
    user = db.Users.find_one({"username": username})
    if user:
        print(f"User found in MongoDB: {username}")
        redis_client.set(f'user:{username}', json.dumps(user, default=str))
    return user


def create_post(title, content, author):
    post = {
        "title": title,
        "content": content,
        "author": author,
        "date_of_creation": datetime.now(),
        "likes": 0,
        "comments": []
    }
    print(f"Creating post: {title}")
    redis_client.set(f'post:{title}', json.dumps(post, default=str))
    result = db.Posts.insert_one(post)
    return result.inserted_id


def delete_post(post_title):
    print(f"Deleting post: {post_title}")
    redis_client.delete(f'post:{post_title}')
    result = db.Posts.delete_one({"title": post_title})
    return result.deleted_count


def get_post(post_title):
    print(f"Getting post: {post_title}")
    cached_post = redis_client.get(f'post:{post_title}')
    if cached_post:
        print(f"Post found in cache: {post_title}")
        return json.loads(cached_post)
    post = db.Posts.find_one({"title": post_title})
    if post:
        print(f"Post found in MongoDB: {post_title}")
        redis_client.set(f'post:{post_title}', json.dumps(post, default=str))
    return post


def create_comment(post_title, content, author):
    comment = {
        "content": content,
        "author": author,
        "date_of_creation": datetime.now(),
        "likes": 0
    }
    liked_post = db.Posts.find_one({"title": post_title})
    if not liked_post:
        print("Post not found")
        return None
    liked_post_author = liked_post["author"]

    send_notification(liked_post_author, "comment", post_title)

    print(f"Creating comment for post {post_title} by {author}")
    redis_client.set(f'comment:{post_title}:{author}', json.dumps(comment, default=str))
    db.Posts.update_one({"title": post_title}, {"$push": {"comments": comment}})
    result = db.Comments.insert_one(comment)
    return result.inserted_id


def get_comment(post_title, author):
    print(f"Getting comment for post {post_title} by {author}")
    cached_comment = redis_client.get(f'comment:{post_title}:{author}')
    if cached_comment:
        print(f"Comment found in cache: post {post_title}, author {author}")
        return json.loads(cached_comment)
    post = db.Comments.find_one({"title": post_title, "author": author})
    if post:
        print(f"Comment found in MongoDB: post {post_title}, author {author}")
        redis_client.set(f'comment:{post_title}:{author}', json.dumps(post, default=str))
    return post


def create_notification(username, notification_type, title):
    notification = {
        "user_id": username,
        "notification_type": notification_type,
        "title": title,
        "created_at": datetime.now()
    }
    print(f"Creating notification for user {username}")
    result = db.Notifications.insert_one(notification)
    return result.inserted_id


def send_notification(username, notification_type, title):
    create_notification(username, notification_type, title)

    try:
        rabbitmq_host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        channel = connection.channel()

        channel.queue_declare(queue=username)

        message = f"notification_type: {notification_type}, title: {title}"
        channel.basic_publish(exchange='', routing_key=username, body=message)

        print(f"Sent notification to {username}: {message}")
        connection.close()
    except Exception as e:
       pass



def create_like(username, post_title):
    print(f"Creating like by {username} for post {post_title}")
    # Find the post with the given title
    liked_post = db.Posts.find_one({"title": post_title})
    if not liked_post:
        print("Post not found")
        return None
    liked_post_author = liked_post["author"]

    send_notification(liked_post_author, "like", post_title)

    db.Posts.update_one({"title": post_title}, {"$inc": {"likes": 1}})

    like = {
        "user_id": username,
        "post_title": post_title,
        "created_at": datetime.now(),
        "user_received": liked_post_author,
    }
    result = db.Likes.insert_one(like)
    return result.inserted_id


def generate_user_activity_report(username):
    print(f"Generating user activity report for {username}")
    user = db.Users.find_one({"username": username})
    if not user:
        return None

    posts_created = db.Posts.count_documents({"author": username})
    comments_created = db.Comments.count_documents({"author": username})
    likes_given = db.Likes.count_documents({"user_id": username})
    likes_received = db.Likes.count_documents({"user_received": username})

    report = {
        "user_id": username,
        "username": user["username"],
        "posts_created": posts_created,
        "comments_created": comments_created,
        "likes_given": likes_given,
        "likes_received": likes_received,
    }

    return report


def delete_all_documents():
    collections = db.list_collection_names()
    for collection in collections:
        db[collection].delete_many({})


def clear_redis():
    redis_client.flushall()
