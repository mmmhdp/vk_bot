from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id
from core.Keyboards.InitKeyboard import InitKeyboard


class EventHandler:
    def __init__(self, vk_api_driver):
        self.__vk = vk_api_driver

    def handle(self, event):
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "Начать":
                    self.init_event(event)

    def init_event(self, event):
        keyboard = InitKeyboard()
        (self.__vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Привет \n"
                    "Выбери тему для теста",
        )
        )
