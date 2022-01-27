from datetime import date, datetime
from flask_login import UserMixin

class Discussion:

    def toDic(self):
        return {'id': self.id, 'topic': self.topic, 'description': self.description, 
                'date': self.date, 'posts': self.posts }

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
                'date': self.date, 'count': self.count, 'description': self.description }

    @staticmethod
    def populate(row):
        aPost = Post()
        aPost.id = row.get('id')
        aPost.title = row.get('title')
        aPost.name = row.get('name')
        aPost.description = row.get('description')
        aPost.date = row.get('date') if row.get('date') is not None else datetime.today().strftime('%d %b %Y')  
        aPost.count = row.get('count') if row.get('count') is not None else 0

        return aPost


class User(UserMixin):
    pass

