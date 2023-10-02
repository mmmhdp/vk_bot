import logging
import sqlite3
from collections import namedtuple
import math


class DataBase:
    logger = logging.getLogger(__name__)

    @classmethod
    def connect(cls):
        try:
            cls.logger.info("connected to db")
            connection = sqlite3.connect("sqlite_db/testing_app.db")
        except sqlite3.OperationalError:
            cls.logger.error("failed to find relative path to sqlite db")
            cls.logger.warning("change path to absolute for db connection")
            connection = sqlite3.connect("core/DataBase/sqlite_db/testing_app.db")

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
        cls.logger.info("get all topics from db")
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
        cls.logger.info("new user added to db")

    @classmethod
    def get_unanswered_question(cls, topic, user_id):
        con = cls.connect()
        cur = con.cursor()
        cur.execute("select ROWID from question left outer join "
                    "("
                    "select question_id from question "
                    "inner join user_question "
                    "ON question.ROWID = user_question.question_id "
                    "WHERE user_question.user_id ="
                    f"'{user_id}'"
                    ") as inside "
                    "ON question.ROWID = inside.question_id "
                    "where question_id IS NULL and topic="
                    f"'{topic}'")
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
            cls.logger.info(f"get unanswered question with id {question.id} from db for user {user_id}")
            return question
        else:
            Question = namedtuple("Question", ["id", "topic", "question", "answer", "link"])
            none_res = [None for _ in range(5)]
            cls.logger.info(f"can't retrieve unanswered question for user {user_id} on topic {topic} from db")
            return Question(*none_res)

    @classmethod
    def add_correct_answer_to_user_score(cls, user_id, question):
        con = cls.connect()
        cur = con.cursor()
        cur.execute("INSERT INTO user_question(user_id, question_id)"
                    f"VALUES ('{user_id}','{question.id}')")
        con.commit()

        cls.logger.info(f"added correct for question with {question.id} for user {user_id} from db")

    @classmethod
    def get_user_statistics(cls, user_id):
        user_statistics = []
        Stats = namedtuple("Stats", ["topic", "ans_percentage"])

        con = cls.connect()
        cur = con.cursor()
        cur.execute("SELECT DISTINCT topic FROM question")
        raw_topics = cur.fetchall()
        for raw_topic in raw_topics:
            topic = raw_topic[0]

            cur.execute("SELECT COUNT(topic) "
                        "FROM question JOIN user_question uq "
                        "ON question.ROWID = uq.question_id "
                        "WHERE question_id IS NOT NULL AND topic="
                        f"'{topic}' "
                        "AND user_id="
                        f"{user_id}")
            raw_num_of_answered_questions_by_topic = cur.fetchall()
            noaqbt = raw_num_of_answered_questions_by_topic[0][0]

            cur.execute("SELECT COUNT(topic) "
                        "FROM question "
                        "WHERE topic="
                        f"'{topic}'")
            raw_total_questions_by_topic = cur.fetchall()
            rqbt = raw_total_questions_by_topic[0][0]

            ans_perc = (noaqbt / rqbt) * 100
            ans_perc = math.trunc(ans_perc)
            topic_stat = Stats(topic, ans_perc)
            user_statistics.append(topic_stat)

        cls.logger.info(f"retrieve stats for user {user_id} from db")
        return user_statistics

    @classmethod
    def have_new_update(cls, user_id):
        con = cls.connect()
        cur = con.cursor()
        cur.execute("SELECT COUNT(rowid) FROM question;")
        raw_num = cur.fetchone()
        curr_num = raw_num[0]
        cur.execute("SELECT last_seen_amount FROM user WHERE vk_user_id="
                    f"'{user_id}'")
        raw_user_num = cur.fetchone()
        user_num = int(raw_user_num[0])

        cls.logger.info(f"checked for updates for user {user_id} from db")

        if curr_num != user_num:
            cur.execute("UPDATE user "
                        "SET last_seen_amount ="
                        f"'{curr_num}'"
                        "where vk_user_id="
                        f"'{user_id}'")
            con.commit()
            return True
        else:
            return False


    # POTENTIAL TEST METHOD
    # @classmethod
    # def add_new_material(cls):
    #     con = cls.connect()
    #     cur = con.cursor()
    #     new_topic = "Математика"
    #     new_questions = ["2+2", "3+3", "5+2"]
    #     new_answers = ["4", "6", "7"]
    #     new_links = ["https://Математика/1", "https://Математика/2", "https://Математика/3"]
    #     for ind in range(len(new_questions)):
    #         cur.execute("INSERT INTO question (topic, question, answer, link) "
    #                     f"VALUES ("
    #                     f"'{new_topic}',"
    #                     f"'{new_questions[ind]}',"
    #                     f"'{new_answers[ind]}',"
    #                     f"'{new_links[ind]}')")
    #         con.commit()
    #     cur.execute("DELETE FROM question WHERE topic='Математика'")
