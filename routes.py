import re
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from jsondb import DiscussionManager
from models import Post, User, Discussion

users = [
    {'tutor@warwick.ac.uk': {'password': '1111', 'is_admin': True }},
    {'student@warwick.ac.uk': {'password': '2222', 'is_admin': False }},
]

def checkUser(email):
    for user in users:
        if email in user:
            return user
    return None

app = Flask(__name__)
app.secret_key = 'This is my secret string' 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(email):
    found = False
    for user in users:
        if email in user:
            found = True
            break
    if found == False: return
    aUser = User()
    aUser.id = email
    aUser.is_admin = user[email]['is_admin']
    return aUser

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('discussion'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('discussion'))

    if request.method == 'GET':
        return render_template('login.html')

    try:
        email = request.form['email']
        user = checkUser(email)

        if user is not None and request.form['password'] == user[email]['password']:
            user = User()
            user.id = email
            login_user(user)

            return redirect(url_for('discussion'))
        else:
            return redirect(url_for('login'))
    except Exception as e:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/')
@app.route('/discussion')
@login_required
def discussion():
    aDManager = DiscussionManager()
    discussions = aDManager.getDiscussions()
    return render_template('discussion.html', discussions=discussions)


@app.route('/list/<int:indexID>')
@login_required
def list(indexID):
    aDManager = DiscussionManager()
    discussion = aDManager.getDiscussion(indexID)
    return render_template('list.html', discussion=discussion)


@app.route('/detail/<int:indexID>/<int:postID>')
@login_required
def detail(indexID, postID):
    aDManager = DiscussionManager()
    aDiscussion = aDManager.getDiscussion(indexID)
    if aDiscussion is not None:
        aPost = aDManager.getDiscussionPost(indexID, postID)
        return render_template('detail.html', discussion=aDiscussion, post=aPost)

    return redirect(url_for('list'))


@app.route('/form')
@app.route('/form/<int:indexID>')
@login_required
def form(indexID=None):
    aDiscussion = None
    if indexID is not None:
        aDManager = DiscussionManager()
        aDiscussion = aDManager.getDiscussion(indexID)

    return render_template('form.html', indexid=indexID, discussion=aDiscussion)


@app.route('/formpost/<int:indexID>')
@app.route('/formpost/<int:indexID>/<int:postID>')
@login_required
def formpost(indexID=None, postID=None):
    aDiscussion = None
    aPost = None
    if indexID is not None:
        aDManager = DiscussionManager()
        aDiscussion = aDManager.getDiscussion(indexID)
        for _idx, _post in enumerate(aDiscussion['posts']):
            if _post['id'] == postID:
                aPost = _post

    return render_template('formpost.html', discussion=aDiscussion, post=aPost)



@app.route('/save', methods=['POST'])
@login_required
def save():
    aDiscussion = Discussion.populate(request.form)
    aDiscussion.name = 'Any Name' # This will be replaced by login name if there is a login function.
    aDManager = DiscussionManager()
    aDManager.insertDiscussion(aDiscussion)

    return redirect(url_for('discussion'))



@app.route('/savepost/<int:indexID>', methods=['GET', 'POST'])
@login_required
def savepost(indexID):
    aPost = Post.populate(request.form)
    aPost.name = 'Any Name' # This will be replaced by login name if there is a login function.
    aDManager = DiscussionManager()
    aDManager.insertPost(indexID, aPost)

    return redirect(url_for('list', indexID=indexID))


@app.route('/update/<int:indexID>', methods=['GET', 'POST'])
@login_required
def update(indexID):
    aDiscussion = Discussion.populate(request.form)
    aDManager = DiscussionManager()
    aDManager.updateDiscussion(indexID, aDiscussion)
    return redirect(url_for('discussion'))


@app.route('/updatepost/<int:indexID>/<int:postID>', methods=['GET', 'POST'])
@login_required
def updatepost(indexID, postID):
    aPost = Post.populate(request.form)
    aDManager = DiscussionManager()
    aDManager.updatePost(indexID, postID, aPost)
    return redirect(url_for('list', indexID=indexID))


@app.route('/delete/<int:indexID>', methods=['GET'])
@login_required
def delete(indexID):
    aDManager = DiscussionManager()
    aDManager.deleteDiscussion(indexID)
    return redirect(url_for('discussion'))


@app.route('/deletepost/<int:indexID>/<int:postID>', methods=['GET'])
@login_required
def deletepost(indexID, postID):
    aDManager = DiscussionManager()
    aDManager.deletePost(indexID, postID)
    return redirect(url_for('list', indexID=indexID))    
