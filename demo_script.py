import time
import requests
from app import dbHelpers as db

base_url = "http://nginx:80"


def demo1():
    # Start with empty database
    db.delete_all_documents()

    # Start with empty cache
    db.clear_redis()

    # Create users
    username1 = db.create_user("Alice", "alice123", "alice@example.com", "password123", "1990-01-01")
    username2 = db.create_user("Bob", "bob123", "bob@example.com", "password123", "1991-01-01")

    # Create a post by user1
    post1_id = db.create_post("Hello, World!", "This is my first post.", username1)

    # Create a comment on post1 by user2
    comment1_id = db.create_comment("Hello, World!", "Nice post, Alice!", username2)

    # Create notifications for user1 (post author) and user2 (comment author)
    # notif1_id = db.create_notification(user1_id, "new_comment", comment1_id)
    # notif2_id = db.create_notification(user2_id, "new_like", post1_id)

    # User2 likes post1
    like1_id = db.create_like(username2, "Hello, World!")

    # Generate user activity report for user1
    report1 = db.generate_user_activity_report(username1)
    print(report1)

    # Generate user activity report for user2
    report2 = db.generate_user_activity_report(username2)
    print(report2)


def demo2():
    # Call create_user function
    new_user = db.create_user("John Doe", "johndoe", "johndoe@example.com", "password123", "1990-01-01")
    print(f"Created user: {new_user}")

    # Call get_user function
    user = db.get_user("johndoe")
    print(f"Retrieved user: {user}")

    # Call create_post function
    post_id = db.create_post("My first post", "This is the content of my first post", "johndoe")
    print(f"Created post with ID: {post_id}")

    # Call get_post function
    post = db.get_post("My first post")
    print(f"Retrieved post: {post}")

    # Call create_comment function
    comment_id = db.create_comment("My first post", "Great post!", "johndoe")
    print(f"Created comment with ID: {comment_id}")

    # Call get_comment function
    comment = db.get_comment("My first post", "johndoe")
    print(f"Retrieved comment: {comment}")

    # Call create_notification function
    notification_id = db.create_notification("johndoe", "post_like", post_id)
    print(f"Created notification with ID: {notification_id}")

    # Call create_like function
    like_id = db.create_like("johndoe", "My first post")
    print(f"Created like with ID: {like_id}")

    # Call generate_user_activity_report function
    report = db.generate_user_activity_report("johndoe")
    print(f"User activity report: {report}")

    # Call delete_post function
    deleted_post_count = db.delete_post("My first post")
    print(f"Deleted {deleted_post_count} posts")

    # Call delete_user function
    deleted_user_count = db.delete_user("johndoe")
    print(f"Deleted {deleted_user_count} users")


def demo3():
    # Create user
    data = {
        "name": "John Doe",
        "username": "johndoe",
        "email": "john@example.com",
        "password": "password123",
        "date_of_birth": "1990-01-01"
    }
    response = requests.post(f"{base_url}/user", json=data)
    print("Create user response:", response.json())

    # Get user
    response = requests.get(f"{base_url}/user/johndoe")
    print("Get user response:", response.json())

    # Create post
    data = {
        "title": "Hello World",
        "content": "This is my first post!",
        "author": "johndoe"
    }
    response = requests.post(f"{base_url}/post", json=data)
    print("Create post response:", response.json())

    # Get post
    response = requests.get(f"{base_url}/post/Hello%20World")
    print("Get post response:", response.json())

    # Create comment
    data = {
        "post_title": "Hello World",
        "content": "Nice post!",
        "author": "johndoe"
    }
    response = requests.post(f"{base_url}/comment", json=data)
    print("Create comment response:", response.json())

    # Get comment
    params = {"post_title": "Hello World", "author": "johndoe"}
    response = requests.get(f"{base_url}/comment", params=params)
    print("Get comment response:", response.json())

    # Create like
    data = {
        "username": "johndoe",
        "post_title": "Hello World"
    }
    response = requests.post(f"{base_url}/like", json=data)
    print("Create like response:", response.json())

    # Generate user activity report
    response = requests.get(f"{base_url}/report/johndoe")
    print("Generate user activity report response:", response.json())

    # Delete post
    data = {"title": "Hello World"}
    response = requests.delete(f"{base_url}/post", json=data)
    print("Delete post response:", response.json())

    # Delete user
    response = requests.delete(f"{base_url}/user/johndoe")
    print("Delete user response:", response.json())


if __name__ == "__main__":
    time.sleep(5)
    print("STARTING DEMO 1")
    demo1()
    print("DEMO 1 COMPLETE\n\n")
    print("STARTING DEMO 2")
    demo2()
    print("DEMO 2 COMPLETE\n\n")
    print("STARTING FLASK DEMO")
    demo3()
    print("FLASK DEMO COMPLETE")
