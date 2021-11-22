from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(LiveServerTestCase):
    """Тест нового посетителя"""

    def setUp(self) -> None:
        """Установка"""
        self.browser = webdriver.Chrome(executable_path='C:\\Users\\Anton\\PythonPJ\\TDD\\chromedriver\\chromedriver.exe')

    def tearDown(self) -> None:
        """Демонтаж"""
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """подтверждение строки в таблице теста"""
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        """тест: можно начать список и получить его позже"""
        self.browser.get(self.live_server_url)

        self.assertEqual('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Купить вагонку')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить гвозди')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')

        self.check_for_row_in_list_table('1: Купить вагонку')
        self.check_for_row_in_list_table('2: Купить гвозди')

        self.fail('Закончить тест!')


# if __name__ == '__main__':
#     unittest.main(warnings='ignore')


