from django.test import TestCase
from parserapp.services import get_area_id

class ServicesTest(TestCase):
    def test_get_area_id(self):
        # Проверяем, что функция возвращает правильный ID для известного региона
        moscow_id = get_area_id('Москва')
        self.assertEqual(moscow_id, '1')  # Ожидаем строку '1'

        # Проверяем, что функция возвращает None для неизвестного региона
        unknown_id = get_area_id('Несуществующий регион')
        self.assertIsNone(unknown_id)