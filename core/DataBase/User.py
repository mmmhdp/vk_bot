class User:
    users = {}

    @classmethod
    def add_user(cls, user_id):
        if user_id not in cls.users:
            User.users[user_id] = {
                "current_topic": "Empty",
                "last_question": "Empty"
            }

    @classmethod
    def get_current_topic(cls, user_id):
        if user_id not in cls.users:
            cls.add_user(user_id)
        return cls.users[user_id]["current_topic"]

    @classmethod
    def update_current_topic(cls, user_id, new_topic):
        pass

    @classmethod
    def get_last_question(cls, user_id):
        pass

    @classmethod
    def update_last_question(cls, user_id, new_question):
        pass
