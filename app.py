
from flask import Flask, request, render_template, redirect, flash, url_for
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "4534gdghjk5d#$RGR^HDG"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


# TODO Create flask app


@app.route('/')
def list_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)


@app.route('/tags')
def display_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/create_tag', methods=['GET', 'POST'])
def add_tag():
    if request.method == 'POST':
        tag_name = request.form['name']
        new_tag = Tag(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect(url_for('display_tags'))
        # return render_template('tags.html', new_tag=new_tag)
    else:
        return render_template('create_tag.html')


@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.commit()
        return redirect('/tags')
    else:
        return render_template('edit_tag.html', tag=tag)


# @app.route('/tags/<int:tag_id>/posts')
# def tag_posts(tag_id):
#     tag = Tag.query.get_or_404(tag_id)
#     posts = tag.project
#     return render_template('tag_posts.html', tag=tag, posts=posts)
@app.route('/tags/<int:tag_id>/posts')
def tag_posts(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.project
    return render_template('tag_posts.html', tag=tag, posts=posts)


@app.route('/', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/{new_user.id}')


@app.route('/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('details.html', user=user, posts=posts)


@app.route('/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/<int:user_id>/add')
def add_blog_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('addpost.html', user=user, tags=tags)


@app.route('/<int:user_id>/add', methods=['POST'])
def add_blog(user_id):
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist['name']

    user_id = user_id

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)

    db.session.commit()

    for tag in tags:
        new_post_tag = PostTag(post_id=new_post.id, tag_id=tag.id)
        db.session.add(new_post_tag)
        db.session.commit()
    return redirect(f'/{user_id}')


@app.route('/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect(f'/{user_id}')


@app.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tag.all()
    return render_template('post_details.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash(f'Post {post.title} deleted.')
    return redirect('/')


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()
    flash(f"Post '{post.title}' has been updated.", "success")
    return redirect('/')
