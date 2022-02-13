from datetime import date, datetime
from flask_login import UserMixin

class NoticeBoard:

    def toDic(self):
        return {'id': self.id, 'title': self.title, 'moduleLink': self.moduleLink, 
                'date': self.date, 'notices': self.notices }

    # Defines notice board metadata structure for storage
    @staticmethod
    def populate(row):
        aNoticeBoard = NoticeBoard()
        aNoticeBoard.id = row.get('id')
        aNoticeBoard.title = row.get('title')
        aNoticeBoard.moduleLink = row.get('moduleLink')
        aNoticeBoard.date = row.get('date') if row.get('date') is not None else datetime.today().strftime('%Y-%m-%d')  
        aNoticeBoard.notices = row.get('notices') if row.get('notices') is not None else []

        return aNoticeBoard


class Notice:
    def toDic(self):
        return {'id': self.id, 'title': self.title, 'name': self.name, 
                'date': self.date, 'count': self.count, 'description': self.description, 'noticePriority': self.noticePriority, 'comments': self.comments }

    # Define notice metadata structure for storage
    @staticmethod
    def populate(row):
        aNotice = Notice()
        aNotice.id = row.get('id')
        aNotice.title = row.get('title')
        aNotice.name = row.get('name')
        aNotice.description = row.get('description')
        aNotice.date = row.get('date') if row.get('date') is not None else datetime.today().strftime('%d %b %Y')  
        aNotice.count = row.get('count') if row.get('count') is not None else 0
        aNotice.noticePriority = row.get('noticePriority')
        aNotice.comments = row.get('comments') if row.get('notices') is not None else []

        return aNotice


class Comment:
    def toDic(self):
        # return {'id': self.id, 'comment': self.comment, 'date': self.date, 'replyStatus': self.replyStatus}
        return {'id': self.id, 'comment': self.comment, 'date': self.date,'replies': self.replies}

    # Define post metadata structure for storage
    @staticmethod
    def populate(row):
        aComment = Comment()
        aComment.id = row.get('id')
        aComment.comment = row.get('comment')
        aComment.date = row.get('date') if row.get('date') is not None else datetime.today().strftime('%d %b %Y')
        aComment.replies = row.get('replies') if row.get('replies') is not None else []

        return aComment
       

class User(UserMixin):
    pass

class Reply:
    def toDic(self):
        return {'id': self.id, 'reply': self.reply, 'date': self.date}

    # Define reply metadata structure for storage
    @staticmethod
    def populate(row):
        aReply = Reply()
        aReply.id = row.get('id')
        aReply.reply = row.get('reply')
        aReply.date = row.get('date') if row.get('date') is not None else datetime.today().strftime('%d %b %Y')

        return aReply
       