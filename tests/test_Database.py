import sqlite3
from core.Database.Database import DataBase
import pytest


class TestDatabase:
    @pytest.fixture()
    def get_connection(self):
        connection = DataBase.connect()
        return connection

    @pytest.fixture(params=["1", "2", "3"])
    def get_mock_user_id(self, request, get_connection):
        user_id = request.param

        def remove_user_from_db():
            cur = get_connection.cursor()
            cur.execute(f"delete from user where vk_user_id="
                        f"'{user_id}'")
            get_connection.commit()

        request.addfinalizer(remove_user_from_db)

        return user_id

    @staticmethod
    def test_connect():
        con = None
        try:
            con = DataBase.connect()
            return con
        except sqlite3.OperationalError:
            return con

    def test_add_user(self, get_mock_user_id, get_connection):
        user_id = get_mock_user_id

        DataBase.add_user(user_id)

        cur = get_connection.cursor()
        retrieve_user_from_db = cur.execute("select * from user where vk_user_id="
                                            f"{get_mock_user_id}").fetchone()

        assert user_id == retrieve_user_from_db[0]

    def test_get_topics(self, get_connection):
        pass

    def test_unanswered_questions(self):
        pass

    def test_add_correct_answer_to_user_score(self):
        pass

    def test_get_user_statistics(self):
        pass

    @pytest.fixture
    def create_mock_update(self, get_connection):
        new_topic = "Математика"
        new_questions = ["2+2", "3+3", "5+2"]
        new_answers = ["4", "6", "7"]
        new_links = ["https://Математика/1", "https://Математика/2", "https://Математика/3"]

        con = get_connection
        cur = con.cursor()
        for ind in range(len(new_questions)):
            cur.execute("INSERT INTO question (topic, question, answer, link) "
                        f"VALUES ("
                        f"'{new_topic}',"
                        f"'{new_questions[ind]}',"
                        f"'{new_answers[ind]}',"
                        f"'{new_links[ind]}')")
            con.commit()
        yield
        cur.execute("DELETE FROM question WHERE topic='Математика'")
        con.commit()

    @pytest.fixture(params=["1", "2", "3"])
    def create_mock_user(self, request, get_connection):
        user_id = request.param

        con = get_connection
        cur = con.cursor()
        cur.execute("insert into user (vk_user_id) "
                    "values "
                    f"('{user_id}')")
        con.commit()
        yield user_id
        cur.execute("delete from user "
                    "where vk_user_id="
                    f"{user_id}")
        con.commit()
        cur.close()

    def test_have_new_update(self, create_mock_update, create_mock_user):
        assert DataBase.have_new_update(create_mock_user)
