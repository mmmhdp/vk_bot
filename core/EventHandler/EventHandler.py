import logging

from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id
from core.Keyboard.Keyboard import Keyboard
from core.Database.Database import DataBase


class EventHandler:
    def __init__(self, vk_api_driver):
        self.__vk = vk_api_driver
        self.__curr_user_id = None
        self.__last_asked_question = None
        self.__logger = logging.getLogger(__name__)

    def handle(self, event):

        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                self.__curr_user_id = event.user_id

                DataBase.add_user(self.__curr_user_id)

                new_update_flag = DataBase.have_new_update(self.__curr_user_id)

                if new_update_flag:
                    self.update_notification()
                    self.__logger.debug(f"user with user_id {self.__curr_user_id} notified about updates")

                elif request == "Начать":
                    self.init()
                    self.__logger.debug(f"user with user_id {self.__curr_user_id} started session")

                elif request == "Пройти тест по теме":
                    self.show_all_topics()
                    self.__logger.debug(f"user with user_id {self.__curr_user_id} chose test section")

                elif request in DataBase.get_topics():
                    self.__logger.debug(f"user with user_id {self.__curr_user_id} pick the topic {request}")
                    self.give_question_to_think_on(request)

                elif request == "Моя статистика":
                    self.show_stats()
                    self.__logger.debug(f"user with user_id {self.__curr_user_id} asked for stats")

                else:
                    if self.is_message_before_last_is_valid_question_message():
                        self.check_answer(request)

                    else:
                        self.handle_incorrect_input()
                        self.__logger.debug(f"user with user_id {self.__curr_user_id} gives wrong input")

    def is_message_before_last_is_valid_question_message(self):
        if not self.__last_asked_question:
            return False

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
        keyboard = Keyboard.get_keyboard_with_all_topics()
        self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=self.__curr_user_id,
            random_id=get_random_id(),
            message="На данный момент доступны тесты только по данным темам.",
        )

    def give_question_to_think_on(self, topic):
        question = DataBase.get_unanswered_question(topic, self.__curr_user_id)
        if not question.question:
            keyboard = Keyboard.get_keyboard_with_all_topics()
            self.__logger.debug(f"user with user_id {self.__curr_user_id} end questions on topic {topic}")

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
            self.__logger.debug(f"user with user_id {self.__curr_user_id} get question with id {question.id}")

            keyboard = Keyboard.get_basic_keyboard()

            self.__vk.messages.send(
                keyboard=keyboard.get_empty_keyboard(),
                user_id=self.__curr_user_id,
                random_id=get_random_id(),
                message=f"Вопрос: {question.question}?",
            )

    def check_answer(self, answer):
        keyboard = Keyboard.get_keyboard_with_all_topics()
        if answer.lower() == self.__last_asked_question.answer.lower():
            self.__logger.debug(f"user with user_id {self.__curr_user_id}"
                                f" gives right answer on question with id {self.__last_asked_question.id}")
            self.__vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=self.__curr_user_id,
                random_id=get_random_id(),
                message="Верно. Но у меня ещё много вопросов.",
            )
            DataBase.add_correct_answer_to_user_score(self.__curr_user_id, self.__last_asked_question)

        else:
            self.__logger.debug(f"user with user_id {self.__curr_user_id} "
                                f"gives wrong answer on question with id {self.__last_asked_question.id}")

            self.__vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=self.__curr_user_id,
                random_id=get_random_id(),
                message="Ответ неверен. Попробуй узнать больше по ссылке и возвращайся к вопросу позже.\n"
                        f"{self.__last_asked_question.link}"
            )
        self.__last_asked_question = ""

    def handle_incorrect_input(self):
        keyboard = Keyboard.get_init_keyboard()
        self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=self.__curr_user_id,
            random_id=get_random_id(),
            message="Кажется, что с этим я не могу вам помочь в данный момент.\n"
                    "Но возможно, вам будут интересны другие возможности бота."
        )

    def show_stats(self):
        user_name = self.__vk.users.get(user_ids=(self.__curr_user_id))[0]["first_name"]
        keyboard = Keyboard.get_init_keyboard()
        stats = DataBase.get_user_statistics(self.__curr_user_id)
        self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=self.__curr_user_id,
            random_id=get_random_id(),
            message=f"Вот твои текущие результаты, {user_name}: "
        )
        for st_for_topic in stats:
            self.__vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=self.__curr_user_id,
                random_id=get_random_id(),
                message=f"По теме {st_for_topic.topic} процент успешных ответов \n "
                        f"равен {st_for_topic.ans_percentage} %!"
            )

    def update_notification(self):
        keyboard = Keyboard.get_init_keyboard()
        user_name = self.__vk.users.get(user_ids=(self.__curr_user_id))[0]["first_name"]
        self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=self.__curr_user_id,
            random_id=get_random_id(),
            message=f"Приветствую {user_name}!\n"
                    "Рады вам сообщить, что банк вопросов нашего бота пополнен.\n"
                    "Желаем удачи в новых челленджах!",
        )
