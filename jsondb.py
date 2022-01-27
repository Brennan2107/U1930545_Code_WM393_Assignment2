import json

class DiscussionManager:
    JSON_FILE = 'data.json'

    def __init__(self):
        self.__discussions = self.loadJSONDB()


    def loadJSONDB(self):
        with open(DiscussionManager.JSON_FILE) as f:
            return json.load(f)


    def saveDiscussions(self, discussions):
        with open(DiscussionManager.JSON_FILE, 'w') as f:
            json.dump(discussions, f)


    def getDiscussions(self):
        return self.__discussions


    def getDiscussion(self, indexID):
        for _idx, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']:
                return _discussion
        return None


    def getDiscussionPost(self, indexID, postID):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']:
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        _post['count'] += 1
                        self.saveDiscussions(self.__discussions)
                        return _post
        return None


    def insertDiscussion(self, aDiscussion):
        aDiscussion.id = self.__discussions[0]['id'] + 1
        self.__discussions.insert(0, aDiscussion.toDic())
        self.saveDiscussions(self.__discussions)


    def insertPost(self, indexID, aPost):
        aDiscussion = self.getDiscussion(indexID)
        aPost.id = aDiscussion['posts'][0]['id'] + 1 if len(aDiscussion['posts']) != 0 else 1
        aDiscussion['posts'].insert(0, aPost.toDic())
        self.saveDiscussions(self.__discussions)


    def updateDiscussion(self, indexID, aDiscussion):
        for _idx, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']: 
                self.__discussions[_idx]['topic'] = aDiscussion.topic
                self.__discussions[_idx]['description'] = aDiscussion.description
        self.saveDiscussions(self.__discussions)                


    def updatePost(self, indexID, postID, aPost):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']: 
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        self.__discussions[_idx1]['posts'][_idx2]['title'] = aPost.title
                        self.__discussions[_idx1]['posts'][_idx2]['description'] = aPost.description
        self.saveDiscussions(self.__discussions)  


    def deleteDiscussion(self, indexID):
        for _idx, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']: 
                del self.__discussions[_idx]
        self.saveDiscussions(self.__discussions)


    def deletePost(self, indexID, postID):
        for _idx1, _discussion in enumerate(self.__discussions):
            if indexID == _discussion['id']: 
                for _idx2, _post in enumerate(_discussion['posts']):
                    if postID == _post['id']:
                        del self.__discussions[_idx1]['posts'][_idx2]
        self.saveDiscussions(self.__discussions)
