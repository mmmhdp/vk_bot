import sqlite3
from collections import namedtuple
from typing import List, Any


class DataBase:

    @staticmethod
    def connect():
        connection = sqlite3.connect("core/DataBase/sqlite_db/testing_app.db")
        # connection = sqlite3.connect("sqlite_db/testing_app.db")
        return connection

    @classmethod
    def get_topics(cls):
        con = cls.connect()
        cur = con.cursor()
        raw_topics_cur = cur.execute("SELECT topic FROM question")
        raw_topics = raw_topics_cur.fetchall()
        all_topics = set()
        for topic in raw_topics:
            all_topics.add(*topic)
        return all_topics

    @classmethod
    def add_user(cls, user_id):
        con = cls.connect()
        cur = con.cursor()
        cur.execute(f"INSERT INTO user (vk_user_id)"
                    f" VALUES ({user_id})"
                    f"ON CONFLICT(vk_user_id)"
                    f"DO NOTHING")
        con.commit()

    @classmethod
    def get_unanswered_question(cls, topic):
        con = cls.connect()
        cur = con.cursor()
        cur.execute("select ROWID from question left outer join "
                    "("
                    "select question_id from question "
                    "inner join user_question "
                    "ON question.ROWID = user_question.question_id"
                    ") as inside "
                    "ON question.ROWID = inside.question_id where question_id IS NULL and topic="
                    + f"'{topic}'")
        not_answered_questions: list[str] = cur.fetchall()
        if not_answered_questions:
            q_id = int(*not_answered_questions[0])
            cur.execute(f"select rowid, topic, question, answer, link "
                        "from question "
                        "where ROWID="
                        + f"'{q_id}'")
            raw_question = cur.fetchall()
            Question = namedtuple("Question", ["id", "topic", "question", "answer", "link"])
            question = Question(*raw_question[0])
            return question
        else:
            Question = namedtuple("Question", ["id", "topic", "question", "answer", "link"])
            none_res = [None for _ in range(5)]
            return Question(*none_res)

    @classmethod
    def add_correct_answer_to_user_score(cls, user_id, question):
        con = cls.connect()
        cur = con.cursor()
        cur.execute("INSERT INTO user_question(user_id, question_id)"
                    f"VALUES ('{user_id}','{question.id}')")
        con.commit()
