import json

import pytest
import vk_api.keyboard

from core.Keyboard.Keyboard import Keyboard
from core.Database.Database import DataBase


class TestKeyboard:
    def test_get_basic_keyboard(self):
        keyboard = Keyboard.get_basic_keyboard()
        assert isinstance(keyboard, vk_api.keyboard.VkKeyboard)

    def test_get_init_keyboard(self):
        init_keyboard = Keyboard.get_init_keyboard()

        button_one_label, button_two_label = (
            self.get_labels_for_first_and_second_button_from_keyboard(init_keyboard))

        assert button_one_label == "Пройти тест по теме" and button_two_label == "Моя статистика"

    @staticmethod
    def get_labels_for_first_and_second_button_from_keyboard(keyboard):
        keyboard_json = keyboard.get_keyboard()
        keyboard_serialized = json.loads(keyboard_json)

        button_one_label = keyboard_serialized['buttons'][0][0]["action"]["label"]
        button_two_label = keyboard_serialized['buttons'][1][0]["action"]["label"]

        return button_one_label, button_two_label

    @pytest.fixture
    def db_topics_and_permanent_label(self):
        topics = DataBase.get_topics()
        topics.add("Моя статистика")
        return topics

    @classmethod
    def test_get_keyboard_with_all_topics(cls, db_topics_and_permanent_label):
        keyboard = Keyboard.get_keyboard_with_all_topics()

        keyboard_labels_with_topics = cls.get_all_labels_from_keyboard(keyboard)
        assert keyboard_labels_with_topics == db_topics_and_permanent_label

    @staticmethod
    def get_all_labels_from_keyboard(keyboard):
        keyboard_json = keyboard.get_keyboard()
        keyboard_serialized = json.loads(keyboard_json)

        lines = keyboard_serialized['buttons']
        labels = set()
        for single_line_with_buttons in lines:
            for button in single_line_with_buttons:
                labels.add(button["action"]["label"])
        return labels
