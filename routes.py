import re
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from jsondb import NoticeManager
from models import Notice, User, NoticeBoard, Comment, Reply

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
        return redirect(url_for('noticeBoardHomePage'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('noticeBoardHomePage'))

    if request.method == 'GET':
        return render_template('login.html')

    try:
        email = request.form['email']
        user = checkUser(email)

        if user is not None and request.form['password'] == user[email]['password']:
            user = User()
            user.id = email
            login_user(user)

            return redirect(url_for('noticeBoardHomePage'))
        else:
            return redirect(url_for('login'))
    except Exception as e:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# renders noticeBoardHomePage
@app.route('/')
@app.route('/noticeBoardHomePage')
@login_required
def noticeBoardHomePage():
    aDManager = NoticeManager()
    noticeBoards = aDManager.getNoticeBoards()
    return render_template('noticeBoardHomePage.html', noticeBoards=noticeBoards)

# renders the posts list for a specific notice board
@app.route('/noticeList/<int:indexID>')
@login_required
def noticeList(indexID):
    aDManager = NoticeManager()
    noticeBoard = aDManager.getNoticeBoard(indexID)
    return render_template('noticeList.html', noticeBoard=noticeBoard)

# renders the detail view for a specific post on a specific notice board
@app.route('/noticeCommentPage/<int:indexID>/<int:noticeID>')
@login_required
def noticeCommentPage(indexID, noticeID):
    aDManager = NoticeManager()
    aNoticeBoard = aDManager.getNoticeBoard(indexID)
    if aNoticeBoard is not None:
        aNotice = aDManager.getNotice(indexID, noticeID)
        return render_template('noticeCommentPage.html', noticeBoard=aNoticeBoard, notice=aNotice)

    return redirect(url_for('noticeList'))

# renders the form view to allow tutors to be able to create and modify notice board
@app.route('/noticeBoardEditor')
@app.route('/noticeBoardEditor/<int:indexID>')
@login_required
def noticeBoardEditor(indexID=None):
    aNoticeBoard = None
    if indexID is not None:
        aDManager = NoticeManager()
        aNoticeBoard = aDManager.getNoticeBoard(indexID)

    return render_template('noticeBoardEditor.html', indexid=indexID, noticeBoard=aNoticeBoard)

# renders the noticeEditor view to be able to create a new post on a specific board
@app.route('/noticeEditor/<int:indexID>')
@app.route('/noticeEditor/<int:indexID>/<int:noticeID>')
@login_required
def noticeEditor(indexID=None, noticeID=None):
    aNoticeBoard = None
    aNotice = None
    if indexID is not None:
        aDManager = NoticeManager()
        aNoticeBoard = aDManager.getNoticeBoard(indexID)
        for _idx, _notice in enumerate(aNoticeBoard['notices']):
            if _notice['id'] == noticeID:
                aNotice = _notice

    return render_template('noticeEditor.html', noticeBoard=aNoticeBoard, notice=aNotice)



@app.route('/save', methods=['POST'])
@login_required
def save():
    aNoticeBoard = NoticeBoard.populate(request.form)
    aNoticeBoard.name = 'Any Name' # This will be replaced by login name if there is a login function.
    aDManager = NoticeManager()
    aDManager.insertNoticeBoard(aNoticeBoard)

    return redirect(url_for('noticeBoardHomePage'))



@app.route('/savenotice/<int:indexID>', methods=['GET', 'POST'])
@login_required
def savenotice(indexID):
    aNotice = Notice.populate(request.form)
    aNotice.name = 'Any Name' # This will be replaced by login name if there is a login function.
    aDManager = NoticeManager()
    aDManager.insertNotice(indexID, aNotice)

    return redirect(url_for('noticeList', indexID=indexID))


@app.route('/update/<int:indexID>', methods=['GET', 'POST'])
@login_required
def update(indexID):
    aNoticeBoard = NoticeBoard.populate(request.form)
    aDManager = NoticeManager()
    aDManager.updateNoticeBoard(indexID, aNoticeBoard)
    return redirect(url_for('noticeBoardHomePage'))


@app.route('/updatenotice/<int:indexID>/<int:noticeID>', methods=['GET', 'POST'])
@login_required
def updatenotice(indexID, noticeID):
    aNotice = Notice.populate(request.form)
    aDManager = NoticeManager()
    aDManager.updateNotice(indexID, noticeID, aNotice)
    return redirect(url_for('noticeList', indexID=indexID))


@app.route('/delete/<int:indexID>', methods=['GET'])
@login_required
def delete(indexID):
    aDManager = NoticeManager()
    aDManager.deleteNoticeBoard(indexID)
    return redirect(url_for('noticeBoardHomePage'))


@app.route('/deletenotice/<int:indexID>/<int:noticeID>', methods=['GET'])
@login_required
def deletenotice(indexID, noticeID):
    aDManager = NoticeManager()
    aDManager.deleteNotice(indexID, noticeID)
    return redirect(url_for('noticeList', indexID=indexID))    


# When Reply button is clicked for a specific student's comment on a specific notice on a specific board, the specific replies window is opened for that comment


# renders the reply window
@app.route('/reply/<int:indexID>/<int:noticeID>/<int:commentID>')
@login_required
def reply(indexID, noticeID, commentID):
    aDManager = NoticeManager()
    aNoticeBoard = aDManager.getNoticeBoard(indexID)
    if aNoticeBoard is not None:
        aNotice = aDManager.getNotice(indexID, noticeID)
        aComment = aDManager.getNoticeComments(indexID, noticeID, commentID)
        return render_template('reply.html', noticeBoard=aNoticeBoard, notice=aNotice, comment=aComment)

    return redirect(url_for('noticeCommentPage'))






# Triggers the savecomment for a new comment to a post
@app.route('/savecomment/<int:indexID>/<int:noticeID>', methods=['GET', 'POST'])
@login_required
def savecomment(indexID, noticeID):
    aComment = Comment.populate(request.form)
    aDManager = NoticeManager()
    aDManager.insertComment(indexID, noticeID, aComment)
    # Change this to redirect to detail page
    return redirect(url_for('noticeCommentPage', indexID=indexID, noticeID=noticeID))


# Triggers the savereply for a new reply to a comment
@app.route('/savereply/<int:indexID>/<int:noticeID>/<int:commentID>', methods=['GET', 'POST'])
@login_required
def savereply(indexID, noticeID, commentID):
    aReply = Reply.populate(request.form)
    aDManager = NoticeManager()
    aDManager.insertReply(indexID, noticeID, commentID, aReply)
    # Change this to redirect to detail page
    return redirect(url_for('reply', indexID=indexID, noticeID=noticeID, commentID=commentID))    