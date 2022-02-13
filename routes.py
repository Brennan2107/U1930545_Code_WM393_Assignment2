import re
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from jsondb import NoticeManager
from models import Notice, User, NoticeBoard, Comment, Reply

# Available user profiles
users = [
    {'U1010101': {'password': 'tutor', 'is_admin': True }},
    {'U1930545': {'password': 'student', 'is_admin': False }},
]

# Chekcs that the entered user ID is in the list of users
def checkUser(email):
    for user in users:
        if email in user:
            return user
    return None

# LoginManager definitions
app = Flask(__name__)
app.secret_key = 'This is my secret string' 
login_manager = LoginManager()
login_manager.init_app(app)

# Return the user for entered ID
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

# Redirect to login page if not a user
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

# If user is authenticated take to noticeBoardHomePage
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('noticeBoardHomePage'))
    else:
        return redirect(url_for('login'))

# Verifies that the user password is correct for the user id passed in 
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

# Logout functionality, redirect to login page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# renders noticeBoardHomePage by getting notice board from data.json file
@app.route('/')
@app.route('/noticeBoardHomePage')
@login_required
def noticeBoardHomePage():
    aDManager = NoticeManager()
    noticeBoards = aDManager.getNoticeBoards()
    return render_template('noticeBoardHomePage.html', noticeBoards=noticeBoards)

# renders the notice list for a specific notice board
@app.route('/noticeList/<int:indexID>')
@login_required
def noticeList(indexID):
    aDManager = NoticeManager()
    noticeBoard = aDManager.getNoticeBoard(indexID)
    return render_template('noticeList.html', noticeBoard=noticeBoard)

# renders the detail view for a specific notice on a specific notice board
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

# renders the noticeEditor view to be able to create a new notice on a specific notice board
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

# saves a new notice board by taking the new title and moduleLink from text-entries and runs insertNoticeBoard function
@app.route('/save', methods=['POST'])
@login_required
def save():
    aNoticeBoard = NoticeBoard.populate(request.form)
    aNoticeBoard.name = 'Any Name' 
    aDManager = NoticeManager()
    aDManager.insertNoticeBoard(aNoticeBoard)

    return redirect(url_for('noticeBoardHomePage'))

# saves a new notice board by taking the title and description from text-entries and runs insertNotice function
@app.route('/savenotice/<int:indexID>', methods=['GET', 'POST'])
@login_required
def savenotice(indexID):
    aNotice = Notice.populate(request.form)
    aNotice.name = 'Any Name' 
    aDManager = NoticeManager()
    aDManager.insertNotice(indexID, aNotice)

    return redirect(url_for('noticeList', indexID=indexID))

# updates a notice board for new title or moduleLink if an indexID is passed in
@app.route('/update/<int:indexID>', methods=['GET', 'POST'])
@login_required
def update(indexID):
    aNoticeBoard = NoticeBoard.populate(request.form)
    aDManager = NoticeManager()
    aDManager.updateNoticeBoard(indexID, aNoticeBoard)
    return redirect(url_for('noticeBoardHomePage'))

# updates a notice for current indexID and noticeID value
@app.route('/updatenotice/<int:indexID>/<int:noticeID>', methods=['GET', 'POST'])
@login_required
def updatenotice(indexID, noticeID):
    aNotice = Notice.populate(request.form)
    aDManager = NoticeManager()
    aDManager.updateNotice(indexID, noticeID, aNotice)
    return redirect(url_for('noticeList', indexID=indexID))

# removes the notice board with id=indexID
@app.route('/delete/<int:indexID>', methods=['GET'])
@login_required
def delete(indexID):
    aDManager = NoticeManager()
    aDManager.deleteNoticeBoard(indexID)
    return redirect(url_for('noticeBoardHomePage'))

# removes the notice linked to id=indexID and id=noticeID
@app.route('/deletenotice/<int:indexID>/<int:noticeID>', methods=['GET'])
@login_required
def deletenotice(indexID, noticeID):
    aDManager = NoticeManager()
    aDManager.deleteNotice(indexID, noticeID)
    return redirect(url_for('noticeList', indexID=indexID))    


# When Reply button is clicked for a specific student's comment on a specific notice on a specific board, the specific replies window is opened for that comment
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

# Triggers the savecomment for a new comment to a notice
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