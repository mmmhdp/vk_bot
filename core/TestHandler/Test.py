from core.DataBase.DataBase import DataBase


class Test:
    @classmethod
    def get_all_topics(cls):
        return DataBase.get_topics()
