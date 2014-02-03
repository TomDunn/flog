from functools import wraps

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.login import LoginManager, login_user, logout_user, current_user
import markdown

from db import Session
from models.Author import Author
from models.Post import Post

app = Flask(__name__)
app.secret_key = '<YOUR SECRET KEY HERE FOR SECURING USER SESSIONS>'

"""
    Login management
"""

login_manager = LoginManager()
login_manager.init_app(app)

"""
    Routes
"""
@login_manager.user_loader
def load_user(userid):

    if not userid:
        return None

    session = Session()
    user = session.query(Author).filter(Author.id == int(userid)).first()
    session.close()
    return user

def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_anonymous():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_func

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    passwd = request.form['password'] # todo, use wtforms
    email  = request.form['email']

    session = Session() # todo, request based db cntxt
    user    = session.query(Author).filter(Author.email == email).first()
    session.close()

    if user is None or not user.check_passwd(passwd):
        return render_template('login.html')

    login_user(user)
    return render_template('base.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/')
def root():
    print current_user # todo remove
    print current_user.is_anonymous()
    return render_template('base.html')

@app.route('/<post_slug>')
def view_post(post_slug):
    session = Session()
    post    = session.query(Post).filter(Post.slug == post_slug).first()

    session.close()
    return render_template('post.html', post=post, edit=False)

@app.route('/edit/<post_slug>', methods=['GET', 'POST'])
@login_required
def edit_post(post_slug):

    session = Session()
    edit    = True
    post    = session.query(Post).filter(Post.slug == post_slug).first()

    if request.method == 'POST':
        post.set_title(request.form['title'])
        post.body = request.form['body']

        session.add(post)
        session.commit()
        session.refresh(post)

        edit = False

    session.close()
    return render_template('post.html', post=post, edit=edit)

@app.route('/list', methods=['GET'])
def list_posts():
    session = Session()
    posts   = session.query(Post)

    session.close()
    return render_template('list.html', posts=posts)

@app.route('/create', methods=['POST'])
@login_required
def create_post():
    session = Session()
    post = Post.create('woops', sync=True, session=session)
    session.close()

    return post.slug

"""
    Template filters
"""

@app.template_filter('markdown')
def render_markdown(source):
    if source is None:
        return ''

    return markdown.markdown(source)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
