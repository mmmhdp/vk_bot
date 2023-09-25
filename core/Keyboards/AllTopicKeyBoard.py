from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from core.Messages.Test import Test


class AllTopicKeyboard(VkKeyboard):
    def __init__(self):
        super().__init__()
        self.__configurate()

    def __configurate(self):
        self.add_line()
        self.add_button("Темы")
