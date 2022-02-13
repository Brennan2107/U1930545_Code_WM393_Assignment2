import pytest
import requests
from jsondb import NoticeManager
from routes import save
from models import NoticeBoard
from models import Comment
from models import Reply
from datetime import datetime

class TestNoticeBoard:

    # Create new board and check if the number of boards increases by 1
    # Create title and moduleLink are as set as required
    def test_CreateNewBoard(self):

        aDManager = NoticeManager()

        # Get number of boards prior to new notice board addition
        noticeboards = aDManager.getNoticeBoards()
        preNoticeBoardQuantity = len(noticeboards)

        # New notice mock title and module link
        newNoticeTitle = 'TEST_BOARD'
        newNoticeModuleLink = 'WM9999'

        # Define notice board to create
        aNoticeBoard = NoticeBoard()
        aNoticeBoard.id = preNoticeBoardQuantity + 1
        aNoticeBoard.title = newNoticeTitle
        aNoticeBoard.moduleLink = newNoticeModuleLink
        aNoticeBoard.date = datetime.today().strftime('%Y-%m-%d')  
        aNoticeBoard.notices = []

        # Run insertNoticeBoard function for new notice board definition
        aDManager.insertNoticeBoard(aNoticeBoard)

        # Assertion, has the number of notice boards increased by 1
        assert len(noticeboards) == preNoticeBoardQuantity + 1

        # Retrieve updated notice board by passing in new notice board id to getNoticeBoard function
        updatednoticeboard = aDManager.getNoticeBoard(len(noticeboards))

        # Check that new title and moduleLink are as expected
        assert updatednoticeboard['title'] == newNoticeTitle
        assert updatednoticeboard['moduleLink'] == newNoticeModuleLink


    # Ensure that title and moduleLink are as updated to the correct board as required
    def test_UpdateBoard(self):

        aDManager = NoticeManager()

        # Get number of boards prior to new notice board addition
        noticeboards = aDManager.getNoticeBoards()
        preNoticeBoardQuantity = len(noticeboards)

        # New notice mock title and module link
        updatedNoticeTitle = 'TEST_BOARD_UPDATED'
        updatedNoticeModuleLink = 'WM2442'

        # Define notice board to create
        aNoticeBoard = NoticeBoard()
        aNoticeBoard.title = updatedNoticeTitle
        aNoticeBoard.moduleLink = updatedNoticeModuleLink
        aNoticeBoard.date = datetime.today().strftime('%Y-%m-%d')  
        aNoticeBoard.notices = []

        # Run insertNoticeBoard function for new notice board definition
        aDManager.updateNoticeBoard(preNoticeBoardQuantity, aNoticeBoard)

        # Retrieve updated notice board by passing in new notice board id to getNoticeBoard function
        updatednoticeboard = aDManager.getNoticeBoard(len(noticeboards))

        # Check that new title and moduleLink are as expected
        assert updatednoticeboard['title'] == updatedNoticeTitle
        assert updatednoticeboard['moduleLink'] == updatedNoticeModuleLink

    def test_deleteNewBoard(self):

        aDManager = NoticeManager()

        # Find the total number of notice boards, hence the last notice board is the total quantity
        noticeboards = aDManager.getNoticeBoards()
        lastNoticeBoard = len(noticeboards)

        # Call deleteNoticeBoard function and pass in the id of the last board
        aDManager.deleteNoticeBoard(lastNoticeBoard)

        # Get the updated number of boards, this should be 1 less than lastNoticeBoard as 1 board is deleted
        noticeboards = aDManager.getNoticeBoards()
        updatedlastNoticeBoard = len(noticeboards)

        # Assertion, ensure that number of boards 1 less than before the deletion.
        assert updatedlastNoticeBoard == lastNoticeBoard - 1 


class TestNoticeComment:

    # Create new Comment test 
    # Ensure that new comment has the correct text saved against it
    def test_CreateNewComment(self):
        aDManager = NoticeManager()
        
        # Notice location that will be used for comment
        noticeboardID = 1
        noticeID = 4

        # Retrieve Notice data for indexID = noticeboardID and noticeID = noticeID
        originalNoticeMetadata = aDManager.getNotice(noticeboardID, noticeID)

        # Get number of comments on Notice retrieved and add one to access location of new comment
        commentID = len(originalNoticeMetadata['comments']) + 1
        
        # Comment text configuration 
        commenttext = 'testing' + str(commentID)

        # Data for new comment
        aComment = Comment()
        aComment.id = commentID
        aComment.comment = commenttext
        aComment.date = datetime.today().strftime('%d %b %Y')
        aComment.replies = []

        # Run function to insert comment
        aDManager.insertComment(noticeboardID, noticeID, aComment)

        # Retrieve new comment, run the getNoticeComments function
        newComment = aDManager.getNoticeComments(noticeboardID, noticeID, commentID)

        # Assertion, is the newComment equal to commenttext originally passed in
        assert newComment['comment'] == commenttext


class TestCommentReply:

    # Create new Reply test 
    # Ensure that new reply has the correct text saved against it

    def test_CreateNewReply(self):
        aDManager = NoticeManager()
        
        # Notice location that will be used for comment
        noticeboardID = 1
        noticeID = 4
        commentID = 1

        # Retrieve Notice data for indexID = noticeboardID and noticeID = noticeID
        originalCommentMetadata = aDManager.getNoticeComments(noticeboardID, noticeID, commentID)

        # Get number of comments on Notice retrieved and add one to access location of new comment
        replyID = len(originalCommentMetadata['replies']) + 1
        
        # Comment text configuration 
        replytext = 'replyTest' + str(replyID)

        # Data for new comment
        aReply = Reply()
        aReply.id = replyID
        aReply.reply = replytext
        aReply.date = datetime.today().strftime('%d %b %Y')

        # Run function to insert comment
        aDManager.insertReply(noticeboardID, noticeID, commentID, aReply)

        # Retrieve new comment, run the getNoticeComments function
        newReply = aDManager.getCommentReplies(noticeboardID, noticeID, commentID, replyID)
        print(newReply)

        # Assertion, is the newComment equal to commenttext originally passed in
        assert newReply['reply'] == replytext