import json

class NoticeManager:
    JSON_FILE = 'data.json'

    def __init__(self):
        self.__noticeBoards = self.loadJSONDB()

    # Opens JSON file
    def loadJSONDB(self):
        with open(NoticeManager.JSON_FILE) as f:
            return json.load(f)

    # Saves NoticeManager operations to JSON file
    def saveNoticeBoards(self, noticeBoards):
        with open(NoticeManager.JSON_FILE, 'w') as f:
            json.dump(noticeBoards, f)

    # Retrieves all Notice Board data 
    def getNoticeBoards(self):
        return self.__noticeBoards

    # Retrieves individual noticeBoard data for indexID fed in
    def getNoticeBoard(self, indexID):
        for _idx, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']:
                return _NoticeBoard
        return None

    # Retrieves all posts within a NoticeBoard board and if a notice is opened the number of times the notice has been viewed is incremented by 1
    def getNotice(self, indexID, noticeID):
        for _idx1, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']:
                for _idx2, _notice in enumerate(_NoticeBoard['notices']):
                    if noticeID == _notice['id']:
                        _notice['count'] += 1
                        self.saveNoticeBoards(self.__noticeBoards)
                        return _notice
        return None

    # Retrieves all comments on a particular notice on a particular board
    def getNoticeComments(self, indexID, noticeID, commentID):
        for _idx1, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']:
                for _idx2, _notice in enumerate(_NoticeBoard['notices']):
                    if noticeID == _notice['id']:
                        for _idx2, _comment in enumerate(_notice['comments']):
                            if commentID == _comment['id']:
                                return _comment
        return None

     # Retrieves all replies to a particular comment on a particular NoticeBoard on a particular board
    def getCommentReplies(self, indexID, noticeID, commentID, replyID):
        for _idx1, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']:
                for _idx2, _notice in enumerate(_NoticeBoard['notices']):
                    if noticeID == _notice['id']:
                        for _idx2, _comment in enumerate(_notice['comments']):
                            if commentID == _comment['id']:
                                for _idx2, _reply in enumerate(_comment['replies']):
                                    if replyID == _reply['id']:
                                        return _reply
        return None       

    # Creating a new NoticeBoard board
    def insertNoticeBoard(self, aNoticeBoard):
        aNoticeBoard.id = self.__noticeBoards[0]['id'] + 1
        self.__noticeBoards.insert(0, aNoticeBoard.toDic())
        self.saveNoticeBoards(self.__noticeBoards)

    # Creating a new post on a notice board
    # If the post id is not 0, takes the next available post id
    def insertNotice(self, indexID, aNotice):
        aNoticeBoard = self.getNoticeBoard(indexID)
        aNotice.id = aNoticeBoard['notices'][0]['id'] + 1 if len(aNoticeBoard['notices']) != 0 else 1
        aNoticeBoard['notices'].insert(0, aNotice.toDic())
        self.saveNoticeBoards(self.__noticeBoards)

    # Creating a new comment on a post
    # If the post id is not 0, takes the next available post id
    def insertComment(self, indexID, noticeID, aComment):
        aNotice = self.getNotice(indexID, noticeID)
        aComment.id = aNotice['comments'][0]['id'] + 1 if len(aNotice['comments']) != 0 else 1
        aNotice['comments'].insert(0, aComment.toDic())
        self.saveNoticeBoards(self.__noticeBoards)

    # Creating a new reply on a comment
    # If the post id is not 0, takes the next available post id
    def insertReply(self, indexID, noticeID, commentID, aReply):
        aComment = self.getNoticeComments(indexID, noticeID, commentID)
        aReply.id = aComment['replies'][0]['id'] + 1 if len(aComment['replies']) != 0 else 1
        aComment['replies'].insert(0, aReply.toDic())
        self.saveNoticeBoards(self.__noticeBoards)

    # Updating both topic and description fields for the corresponding indexID when a notice board is modified
    # Runs saveNotices function once changes have been made
    def updateNoticeBoard(self, indexID, aNoticeBoard):
        for _idx, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']: 
                self.__noticeBoards[_idx]['title'] = aNoticeBoard.title
                self.__noticeBoards[_idx]['moduleLink'] = aNoticeBoard.moduleLink
        self.saveNoticeBoards(self.__noticeBoards)                

    # Updating both title and description fields for the corresponding postId when a post is modified
    # Runs saveNotices function once changes have been made
    def updateNotice(self, indexID, noticeID, aNotice):
        for _idx1, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']: 
                for _idx2, _notice in enumerate(_NoticeBoard['notices']):
                    if noticeID == _notice['id']:
                        self.__noticeBoards[_idx1]['notices'][_idx2]['title'] = aNotice.title
                        self.__noticeBoards[_idx1]['notices'][_idx2]['description'] = aNotice.description
                        self.__noticeBoards[_idx1]['notices'][_idx2]['noticePriority'] = aNotice.noticePriority
        self.saveNoticeBoards(self.__noticeBoards)  

    # Remove the associated notice from notice ids
    # Save changes by running saveNotices function
    def deleteNoticeBoard(self, indexID):
        for _idx, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']: 
                del self.__noticeBoards[_idx]
        self.saveNoticeBoards(self.__noticeBoards)

    # Remove the associated post from post ids
    # Save changes by running saveNoticeBoards function
    def deleteNotice(self, indexID, noticeID):
        for _idx1, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']: 
                for _idx2, _notice in enumerate(_NoticeBoard['notices']):
                    if noticeID == _notice['id']:
                        del self.__noticeBoards[_idx1]['notices'][_idx2]
        self.saveNoticeBoards(self.__noticeBoards)

    # Remove the associated comment from comment ids
    # Save changes by running saveNotices function
    def deleteComment(self, indexID, noticeID, commentID):
        for _idx1, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']:
                for _idx2, _notice in enumerate(_NoticeBoard['notices']):
                    if noticeID == _notice['id']:
                        for _idx2, _comment in enumerate(_notice['comments']):
                            if commentID == _comment['id']:
                                del self.__noticeBoards[_idx1]['comments'][_idx2]
        self.saveNoticeBoards(self.__noticeBoards)

    # Remove the associated reply from reply ids
    # Save changes by running saveNotices function
    def deleteReply(self, indexID, noticeID, commentID, replyID):
        for _idx1, _NoticeBoard in enumerate(self.__noticeBoards):
            if indexID == _NoticeBoard['id']:
                for _idx2, _notice in enumerate(_NoticeBoard['notices']):
                    if noticeID == _notice['id']:
                        for _idx2, _comment in enumerate(_notice['comments']):
                            if commentID == _comment['id']:
                                for _idx2, _reply in enumerate(_comment['replies']):
                                    if replyID == _reply['id']:
                                       del self.__noticeBoards[_idx1]['replies'][_idx2]
        self.saveNoticeBoards(self.__noticeBoards)   