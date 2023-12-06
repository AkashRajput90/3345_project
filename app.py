from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.routing import BaseConverter

app = Flask(__name__)
client = MongoClient('mongodb://blogdbaccount:DJeiV2yZlFvd2EpoLQNNYCdEwmrgLsy8nkirggYZGHlw2fXSHpCXP7GnijKugivxR24ZW4uhlvTwACDbgxdwUQ==@blogdbaccount.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@blogdbaccount@')  # Connect to your MongoDB instance
db = client['blogdatabase']  # Use or create a database named 'blog_db'
posts_collection = db['posts']  # Create or use a collection named 'posts'

class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(value)
        except:
            raise ValueError()

    def to_url(self, value):
        return str(value)
 
app.url_map.converters['ObjectId'] = ObjectIdConverter

@app.route('/')
def index():
    posts = list(posts_collection.find())  # Retrieve all posts from MongoDB
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = {'title': title, 'content': content}
        posts_collection.insert_one(new_post)  # Insert a new post into MongoDB
        return redirect(url_for('index'))
    return render_template('create_post.html')

@app.route('/edit_post/<ObjectId:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = posts_collection.find_one({'_id': post_id})
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        posts_collection.replace_one({'_id': post_id}, post)  # Update the post in MongoDB
        return redirect(url_for('index'))
    return render_template('edit_post.html', post=post)


@app.route('/delete_post/<ObjectId:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if request.method == 'POST':
        posts_collection.delete_one({'_id': post_id})  # Delete the post from MongoDB
        return redirect(url_for('index'))
    # Handle other cases, like GET requests or invalid post_id
    return "Invalid request"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
