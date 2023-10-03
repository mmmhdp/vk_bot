import sqlite3
from core.Database.Database import DataBase
import pytest
from decouple import config

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

    def test_have_new_update(self):
        pass

