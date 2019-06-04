from flask import render_template, flash, redirect, request
from app import app, db
from app.models import Post
from app.forms import PostForm
import markdown
import random
import string

from flask import Markup


def autoPath():
    charset = string.ascii_lowercase + string.ascii_uppercase + "0123456789"
    return "".join(random.choice(charset) for i in range(4))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new", methods=["GET", "POST"])
def new():
    form = PostForm()
    if form.validate_on_submit():

        if form.path.data == "":

            path = autoPath()
        else:
            path = form.path.data

        p = Post(title=form.title.data, content=form.content.data, path=path)
        db.session.add(p)
        db.session.commit()
        # flash("Your post was correctly uploaded")
        return redirect("/posts/" + path)
    return render_template("newpost.html", form=PostForm())


@app.route("/posts")
def posts():
    postList = Post.query.all()
    return render_template("posts.html", postList=postList)


@app.route("/posts/<path>")
def post(path):
    post = Post.query.filter_by(path=path).first_or_404()
    content = Markup(markdown.markdown(post.content))
    return render_template("post.html", post=post, content=content)

