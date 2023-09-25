from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class InitKeyboard(VkKeyboard):
    def __init__(self):
        super().__init__()
        self.__configurate()

    def __configurate(self):
        self.add_button("Темы")
