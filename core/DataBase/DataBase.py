import sqlite3


class DataBase:
    storage = {}

    @classmethod
    def get_topics(cls):
        con = sqlite3.connect("core/DataBase/sqlite_db/questions.db")
        cur = con.cursor()
        res = cur.execute("SELECT topic FROM question")
        res = res.fetchall()
        all_topics = set()
        for el in res:
            all_topics.add(*el)
        return all_topics
