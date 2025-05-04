from flask import Flask, request, jsonify, session, redirect, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

POSTS_FILE = 'posts.json'
USERS = {'admin': 'password123'}

# Load posts
def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save posts
def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f)

@app.route('/api/posts')
def get_posts():
    return jsonify(load_posts())

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] in USERS and USERS[data['username']] == data['password']:
        session['username'] = data['username']
        return jsonify({'success': True})
    return jsonify({'success': False}), 401

@app.route('/api/post', methods=['POST'])
def create_post():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.json
    posts = load_posts()
    data['id'] = len(posts) + 1
    posts.append(data)
    save_posts(posts)
    return jsonify({'success': True})

@app.route('/post/<int:post_id>')
def show_post(post_id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return "Post not found", 404
    return f"<h1>{post['title']}</h1><p>{post['date']}</p><img src='{post['image']}' width='400'><p>{post['content']}</p>"

if __name__ == '__main__':
    app.run(debug=True)
