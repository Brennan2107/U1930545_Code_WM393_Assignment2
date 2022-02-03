import json

class DiscussionManager:
    JSON_FILE = 'data.json'

    def __init__(self):
        self.__discussions = self.loadJSONDB()

    # Opens JSON file
    def loadJSONDB(self):
        with open(DiscussionManager.JSON_FILE) as f:
            return json.load(f)

    # Saves DiscussionManager operations to JSON file
    def saveDiscussions(self, discussions):
        with open(DiscussionManager.JSON_FILE, 'w') as f:
            json.dump(discussions, f)

    # Retrieves all Discussion data 
    def getDiscussions(self):
        return self.__discussions




    # Retrieves individual discussion data and assigns each discussion to indexID
    def getDiscussion(self, indexID):
        for _idx, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']:
                return _discussion
        return None

    # Retrieves all posts within a discussion board and if a post is opened the number of times the post has been viewed is incremented by 1
    def getDiscussionPost(self, indexID, postID):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']:
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        _post['count'] += 1
                        self.saveDiscussions(self.__discussions)
                        return _post
        return None

    # Retrieves all comments on a particular notice on a particular board
    def getNoticeComments(self, indexID, postID, commentID):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']:
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        for _idx2, _comment in enumerate(_post['comments']):
                            if commentID == _comment['id']:
                                return _comment
        return None


     # Retrieves all replies to a particular comment on a particular notice on a particular board
    def getCommentReplies(self, indexID, postID, commentID, replyID):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']:
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        for _idx2, _comment in enumerate(_post['comments']):
                            if commentID == _comment['id']:
                                for _idx2, _reply in enumerate(_comment['replies']):
                                    if replyID == _reply['id']:
                                        return _reply
        return None       





    # Creating a new discussion board
    def insertDiscussion(self, aDiscussion):
        aDiscussion.id = self.__discussions[0]['id'] + 1
        self.__discussions.insert(0, aDiscussion.toDic())
        self.saveDiscussions(self.__discussions)


    # Creating a new post on a discussion board
    # If the post id is not 0, takes the next available post id
    def insertPost(self, indexID, aPost):
        aDiscussion = self.getDiscussion(indexID)
        aPost.id = aDiscussion['posts'][0]['id'] + 1 if len(aDiscussion['posts']) != 0 else 1
        aDiscussion['posts'].insert(0, aPost.toDic())
        self.saveDiscussions(self.__discussions)


    # Creating a new comment on a post
    # If the post id is not 0, takes the next available post id
    def insertComment(self, indexID, postID, aComment):
        aPost = self.getDiscussionPost(indexID, postID)
        aComment.id = aPost['comments'][0]['id'] + 1 if len(aPost['comments']) != 0 else 1
        aPost['comments'].insert(0, aComment.toDic())
        self.saveDiscussions(self.__discussions)

    # Creating a new reply on a comment
    # If the post id is not 0, takes the next available post id
    def insertReply(self, indexID, postID, commentID, aReply):
        aComment = self.getNoticeComments(indexID, postID, commentID)
        aReply.id = aComment['replies'][0]['id'] + 1 if len(aComment['replies']) != 0 else 1
        aComment['replies'].insert(0, aReply.toDic())
        self.saveDiscussions(self.__discussions)






    # Updating both topic and description fields for the corresponding indexID when a discussion board is modified
    # Runs saveDiscussions function once changes have been made
    def updateDiscussion(self, indexID, aDiscussion):
        for _idx, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']: 
                self.__discussions[_idx]['topic'] = aDiscussion.topic
                self.__discussions[_idx]['description'] = aDiscussion.description
        self.saveDiscussions(self.__discussions)                

    # Updating both title and description fields for the corresponding postId when a post is modified
    # Runs saveDiscussions function once changes have been made
    def updatePost(self, indexID, postID, aPost):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']: 
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        self.__discussions[_idx1]['posts'][_idx2]['title'] = aPost.title
                        self.__discussions[_idx1]['posts'][_idx2]['description'] = aPost.description
                        self.__discussions[_idx1]['posts'][_idx2]['noticePriority'] = aPost.noticePriority
        self.saveDiscussions(self.__discussions)  



    # !!!!! DONT WANT TO BE ABLE TO EDIT COMMENTS !!!!! 



    # Remove the associated discussion from discussion ids
    # Save changes by running saveDiscussions function
    def deleteDiscussion(self, indexID):
        for _idx, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']: 
                del self.__discussions[_idx]
        self.saveDiscussions(self.__discussions)

    # Remove the associated post from post ids
    # Save changes by running saveDiscussions function
    def deletePost(self, indexID, postID):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']: 
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        del self.__discussions[_idx1]['posts'][_idx2]
        self.saveDiscussions(self.__discussions)

    # Remove the associated comment from comment ids
    # Save changes by running saveDiscussions function
    def deleteComment(self, indexID, postID, commentID):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']:
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        for _idx2, _comment in enumerate(_post['comments']):
                            if commentID == _comment['id']:
                                del self.__discussions[_idx1]['comments'][_idx2]
        self.saveDiscussions(self.__discussions)

    # Remove the associated reply from reply ids
    # Save changes by running saveDiscussions function
    def deleteReply(self, indexID, postID, commentID, replyID):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']:
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        for _idx2, _comment in enumerate(_post['comments']):
                            if commentID == _comment['id']:
                                for _idx2, _reply in enumerate(_comment['replies']):
                                    if replyID == _reply['id']:
                                       del self.__discussions[_idx1]['replies'][_idx2]
        self.saveDiscussions(self.__discussions)   