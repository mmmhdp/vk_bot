from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id
from core.Keyboards.Keyboard import Keyboard
from core.DataBase.DataBase import DataBase
import re


class EventHandler:
    def __init__(self, vk_api_driver):
        self.__vk = vk_api_driver
        self.__curr_user_id = None

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

                elif re.search("^Ответ:", request):
                    self.check_answer()

                else:
                    self.incorrect_topic()

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
        print(f"тестиремся ёба по {question}")

    def check_answer(self):
        keyboard = Keyboard.get_all_topics_keyboard()
        self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=self.__curr_user_id,
            random_id=get_random_id(),
            message="Верно/Неверно",
        )

    def incorrect_topic(self):
        keyboard = Keyboard.get_init_keyboard()
        self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=self.__curr_user_id,
            random_id=get_random_id(),
            message="Кажется, что с этим я не могу вам помочь в данный момент.\n"
                    "Но возможно, вам будут интересны другие возможности бота."
        )
