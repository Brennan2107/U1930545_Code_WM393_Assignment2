import pytest
import requests
from jsondb import NoticeManager
from routes import save
from models import NoticeBoard
from datetime import date, datetime

#@pytest.mark.skip
# !!USERSTORYID: NOTICE_US1!! Test that notice board home page is loaded within 3s for students 
def test_NoticeManager():
    aDManager = NoticeManager()
    noticeboards = aDManager.getNoticeBoards()
    assert len(noticeboards) == 4
    assert len(noticeboards) == 5

@pytest.mark.skip
def test_CreateNewBoard():
    aDManager = NoticeManager()

    # Define notice board to create
    aNoticeBoard = NoticeBoard()
    aNoticeBoard.id = 10
    aNoticeBoard.title = 'CREATEboardTEST'
    aNoticeBoard.moduleLink = 'WM9999'
    aNoticeBoard.date = datetime.today().strftime('%Y-%m-%d')  
    aNoticeBoard.notices = []

    boardCreation = aDManager.insertNoticeBoard(aNoticeBoard)


    assert boardCreation.status_code == 200

