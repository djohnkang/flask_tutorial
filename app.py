import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.init_app(app)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

db.create_all()

@app.route("/")
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)
    
@app.route("/create")
def create():
    form_title = request.args.get("title")
    form_content = request.args.get("content")
    post = Post(title=form_title, content=form_content)
    db.session.add(post)
    db.session.commit()
    return render_template('create.html', title=form_title, content=form_content)


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))