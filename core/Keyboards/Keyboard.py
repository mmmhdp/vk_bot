from vk_api.keyboard import VkKeyboard
from core.TestHandler.Test import Test


class Keyboard:
    @classmethod
    def get_init_keyboard(cls):
        keyboard = VkKeyboard()
        keyboard.add_button("Пройти тест по теме")
        return keyboard

    @classmethod
    def get_all_topics_keyboard(cls):
        keyboard = VkKeyboard()
        for ind, topic in enumerate(Test.get_all_topics()):
            keyboard.add_button(f"{topic}")
            if ind % 2 == 1:
                keyboard.add_line()
        return keyboard
