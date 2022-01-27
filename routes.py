from flask import Flask
from flask import render_template, request, redirect, url_for
from jsondb import DiscussionManager
from models import Discussion, Post

app = Flask(__name__)

@app.route('/')
@app.route('/discussion')
def discussion():
    aDManager = DiscussionManager()
    discussions = aDManager.getDiscussions()
    return render_template('discussion.html', discussions=discussions)


@app.route('/list/<int:indexID>')
def list(indexID):
    aDManager = DiscussionManager()
    discussion = aDManager.getDiscussion(indexID)
    return render_template('list.html', discussion=discussion)


@app.route('/detail/<int:indexID>/<int:postID>')
def detail(indexID, postID):
    aDManager = DiscussionManager()
    aDiscussion = aDManager.getDiscussion(indexID)
    if aDiscussion is not None:
        aPost = aDManager.getDiscussionPost(indexID, postID)
        return render_template('detail.html', discussion=aDiscussion, post=aPost)

    return redirect(url_for('list'))


@app.route('/form')
@app.route('/form/<int:indexID>')
def form(indexID=None):
    aDiscussion = None
    if indexID is not None:
        aDManager = DiscussionManager()
        aDiscussion = aDManager.getDiscussion(indexID)

    return render_template('form.html', indexid=indexID, discussion=aDiscussion)


@app.route('/formpost/<int:indexID>')
@app.route('/formpost/<int:indexID>/<int:postID>')
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
def save():
    aDiscussion = Discussion.populate(request.form)
    aDiscussion.name = 'Any Name' # This will be replaced by login name if there is a login function.
    aDManager = DiscussionManager()
    aDManager.insertDiscussion(aDiscussion)

    return redirect(url_for('discussion'))



@app.route('/savepost/<int:indexID>', methods=['GET', 'POST'])
def savepost(indexID):
    aPost = Post.populate(request.form)
    aPost.name = 'Any Name' # This will be replaced by login name if there is a login function.
    aDManager = DiscussionManager()
    aDManager.insertPost(indexID, aPost)

    return redirect(url_for('list', indexID=indexID))


@app.route('/update/<int:indexID>', methods=['GET', 'POST'])
def update(indexID):
    aDiscussion = Discussion.populate(request.form)
    aDManager = DiscussionManager()
    aDManager.updateDiscussion(indexID, aDiscussion)
    return redirect(url_for('discussion'))


@app.route('/updatepost/<int:indexID>/<int:postID>', methods=['GET', 'POST'])
def updatepost(indexID, postID):
    aPost = Post.populate(request.form)
    aDManager = DiscussionManager()
    aDManager.updatePost(indexID, postID, aPost)
    return redirect(url_for('list', indexID=indexID))


@app.route('/delete/<int:indexID>', methods=['GET'])
def delete(indexID):
    aDManager = DiscussionManager()
    aDManager.deleteDiscussion(indexID)
    return redirect(url_for('discussion'))


@app.route('/deletepost/<int:indexID>/<int:postID>', methods=['GET'])
def deletepost(indexID, postID):
    aDManager = DiscussionManager()
    aDManager.deletePost(indexID, postID)
    return redirect(url_for('list', indexID=indexID))    
