# post_service.py
import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory posts data (a dictionary with post IDs as keys)
posts = {
    1: {"user_id": "1", "post": "Hello, world!"},
    2: {"user_id": "2", "post": "My first blog post"},
}


# Function to generate a unique post ID
def generate_post_id():
    return max(posts.keys()) + 1


# Function to fetch user information from the user service
def get_user_info(user_id):
    user_service_url = "http://0.0.0.0:5000/users/" + str(
        user_id
    ) 
    response = requests.get(user_service_url)
    return response.json() if response.status_code == 200 else None


# Create a new post
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    user_id = data.get("user_id")
    user_info = get_user_info(user_id)

    if user_info:
        post_id = generate_post_id()
        new_post = {
            "id": post_id,
            "user_info": user_info,
            "post": data.get("post", "This is a random post."),
        }
        posts[post_id] = new_post
        return jsonify(new_post), 201
    return "User not found", 404


# Get all posts
@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(posts)


# Get a specific post by ID
@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = posts.get(post_id)
    if post is not None:
        return jsonify(post)
    return "Post not found", 404


if __name__ == "__main__":
    app.run(port=5001, debug=True)
