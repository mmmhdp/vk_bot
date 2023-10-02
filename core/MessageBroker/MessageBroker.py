import logging

import vk_api
from vk_api.longpoll import VkLongPoll
from core.EventHandler.EventHandler import EventHandler
from decouple import config


class MessageBroker:
    def __init__(self):
        self.__key = None
        self.__vk_session = None
        self.__longpoll = None
        self.__vk = None
        self.__event_handler = None
        self.__logger = logging.getLogger(__name__)

    def setup(self):
        self.__key = config("VK_BOT_KEY")
        self.__vk_session = vk_api.VkApi(token=self.__key)
        self.__longpoll = VkLongPoll(self.__vk_session)
        self.__vk = self.__vk_session.get_api()
        self.__event_handler = EventHandler(self.__vk)

    def listen(self):
        for event in self.__longpoll.listen():
            self.__event_handler.handle(event)
