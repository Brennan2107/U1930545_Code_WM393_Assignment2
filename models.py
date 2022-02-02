from datetime import date, datetime
from flask_login import UserMixin

class Discussion:

    def toDic(self):
        return {'id': self.id, 'topic': self.topic, 'description': self.description, 
                'date': self.date, 'posts': self.posts }

    # Defines discussion board metadata structure for storage
    @staticmethod
    def populate(row):
        aDiscussion = Discussion()
        aDiscussion.id = row.get('id')
        aDiscussion.topic = row.get('topic')
        aDiscussion.description = row.get('description')
        aDiscussion.date = row.get('date') if row.get('date') is not None else datetime.today().strftime('%Y-%m-%d')  
        aDiscussion.posts = row.get('posts') if row.get('posts') is not None else []

        return aDiscussion


class Post:
    def toDic(self):
        return {'id': self.id, 'title': self.title, 'name': self.name, 
                'date': self.date, 'count': self.count, 'description': self.description, 'comments': self.comments }

    # Define post metadata structure for storage
    @staticmethod
    def populate(row):
        aPost = Post()
        aPost.id = row.get('id')
        aPost.title = row.get('title')
        aPost.name = row.get('name')
        aPost.description = row.get('description')
        aPost.date = row.get('date') if row.get('date') is not None else datetime.today().strftime('%d %b %Y')  
        aPost.count = row.get('count') if row.get('count') is not None else 0
        aPost.comments = row.get('comments') if row.get('posts') is not None else []

        return aPost


class Comment:
    def toDic(self):
        # return {'id': self.id, 'comment': self.comment, 'date': self.date, 'replyStatus': self.replyStatus}
        return {'id': self.id, 'comment': self.comment, 'date': self.date,'replies': self.replies}

    #'replies': self.replies - need to add this back into toDic

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

    # Define post metadata structure for storage
    @staticmethod
    def populate(row):
        aReply = Reply()
        aReply.id = row.get('id')
        aReply.reply = row.get('reply')
        aReply.date = row.get('date') if row.get('date') is not None else datetime.today().strftime('%d %b %Y')

        return aReply
       

class User(UserMixin):
    pass