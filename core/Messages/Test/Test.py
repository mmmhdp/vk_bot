from Topic import Topic


class Test:
    def __init__(self):
        self.counter = 0
        self.__all_topics = {}

    @property
    def all_topics(self):
        return self.__all_topics

    @all_topics.getter
    def all_topics(self):
        return self.__all_topics

    def __add_topics(self, new_topic):
        self.__all_topics[self.counter] = new_topic

    def __remove_topic(self, topic_id):
        del self.__all_topics[topic_id]
