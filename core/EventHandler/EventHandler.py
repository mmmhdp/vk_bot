from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id
from core.Keyboards.Keyboard import Keyboard
from core.DataBase.DataBase import DataBase


class EventHandler:
    def __init__(self, vk_api_driver):
        self.__vk = vk_api_driver
        self.__curr_user_id = None
        self.__last_asked_question = None

    def handle(self, event):
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                self.__curr_user_id = event.user_id

                DataBase.add_user(self.__curr_user_id)

                if request == "Начать":
                    self.init()

                elif request == "Пройти тест по теме":
                    self.show_all_topics()

                elif request in DataBase.get_topics():
                    self.testing(request)

                else:
                    if self.is_message_before_last_is_valid_question_message():
                        self.check_answer(request)

                    else:
                        self.incorrect_topic()

    def is_message_before_last_is_valid_question_message(self):
        bot_last_message = self.__vk.messages.getHistory(count=2,
                                                         user_id=self.__curr_user_id)["items"][1]["text"]
        potential_raw_last_question = self.__last_asked_question.question
        potential_real_last_question = "Вопрос: " + potential_raw_last_question + "?"
        return True if bot_last_message == potential_real_last_question else False

    def init(self):
        keyboard = Keyboard.get_init_keyboard()
        user_name = self.__vk.users.get(user_ids=(self.__curr_user_id))[0]["first_name"]
        self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=self.__curr_user_id,
            random_id=get_random_id(),
            message=f"Привет {user_name}!\n"
                    "Вот текущий функционал нашего бота.",
        )

    def show_all_topics(self):
        keyboard = Keyboard.get_all_topics_keyboard()
        self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=self.__curr_user_id,
            random_id=get_random_id(),
            message="На данный момент доступны тесты только по данным темам.",
        )

    def testing(self, topic):
        question = DataBase.get_unanswered_question(topic)
        if not question.question:
            keyboard = Keyboard.get_all_topics_keyboard()

            self.__vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=self.__curr_user_id,
                random_id=get_random_id(),
                message="Вы ответили верно на все вопросы данной темы. \n"
                        "Поздравляю!\n"
                        "Теперь самое время попытать удачу в других областях знания!",
            )
        else:
            self.__last_asked_question = question

            keyboard = Keyboard.get_empty_keyboard()

            self.__vk.messages.send(
                keyboard=keyboard.get_empty_keyboard(),
                user_id=self.__curr_user_id,
                random_id=get_random_id(),
                message=f"Вопрос: {question.question}?",
            )

    def check_answer(self, answer):
        keyboard = Keyboard.get_all_topics_keyboard()
        if answer.lower() == self.__last_asked_question.answer.lower():
            self.__vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=self.__curr_user_id,
                random_id=get_random_id(),
                message="Верно. Но у меня ещё много вопросов.",
            )
            DataBase.add_correct_answer_to_user_score(self.__curr_user_id, self.__last_asked_question)

        else:
            self.__vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=self.__curr_user_id,
                random_id=get_random_id(),
                message="На, вот, подучи матчасть, там уж и поговорим, да.\n"
                        f"{self.__last_asked_question.link}"
            )
        self.__last_asked_question = None

    def incorrect_topic(self):
        keyboard = Keyboard.get_init_keyboard()
        self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=self.__curr_user_id,
            random_id=get_random_id(),
            message="Кажется, что с этим я не могу вам помочь в данный момент.\n"
                    "Но возможно, вам будут интересны другие возможности бота."
        )
