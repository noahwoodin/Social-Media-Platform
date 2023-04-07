from flask import Flask, request, jsonify
import dbHelpers as db

from datetime import datetime

app = Flask(__name__)


@app.route('/user', methods=['POST'])
def create_user_endpoint():
    data = request.get_json()
    name = data.get("name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    date_of_birth = datetime.strptime(data.get("date_of_birth"), '%Y-%m-%d')
    result = db.create_user(name, username, email, password, date_of_birth)
    return jsonify({"username": result}), 201


@app.route('/user/<string:username>', methods=['GET', 'DELETE'])
def user_endpoint(username):
    if request.method == 'GET':
        result = db.get_user(username)
        return jsonify(result), 200
    elif request.method == 'DELETE':
        result = db.delete_user(username)
        return jsonify({"deleted_count": result}), 200


@app.route('/post', methods=['POST', 'DELETE'])
def post_endpoint():
    data = request.get_json()
    title = data.get("title")
    if request.method == 'POST':
        content = data.get("content")
        author = data.get("author")
        result = db.create_post(title, content, author)
        return jsonify({"post_id": str(result)}), 201
    elif request.method == 'DELETE':
        result = db.delete_post(title)
        return jsonify({"deleted_count": result}), 200


@app.route('/post/<string:title>', methods=['GET'])
def get_post_endpoint(title):
    result = db.get_post(title)
    return jsonify(result), 200


@app.route('/comment', methods=['POST'])
def create_comment_endpoint():
    data = request.get_json()
    post_title = data.get("post_title")
    content = data.get("content")
    author = data.get("author")
    result = db.create_comment(post_title, content, author)
    return jsonify({"comment_id": str(result)}), 201


@app.route('/comment', methods=['GET'])
def get_comment_endpoint():
    post_title = request.args.get("post_title")
    author = request.args.get("author")
    result = db.get_comment(post_title, author)
    return jsonify(result), 200


@app.route('/like', methods=['POST'])
def create_like_endpoint():
    data = request.get_json()
    username = data.get("username")
    post_title = data.get("post_title")
    result = db.create_like(username, post_title)
    return jsonify({"like_id": str(result)}), 201


@app.route('/report/<string:username>', methods=['GET'])
def generate_user_activity_report_endpoint(username):
    result = db.generate_user_activity_report(username)
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
