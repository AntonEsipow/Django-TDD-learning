from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """Тест нового посетителя"""

    def setUp(self) -> None:
        """Установка"""
        self.browser = webdriver.Chrome(executable_path='C:\\Users\\Anton\\PythonPJ\\TDD\\chromedriver\\chromedriver.exe')

    def tearDown(self) -> None:
        """Демонтаж"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """ожидать строку в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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
        # time.sleep(1)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить гвозди')
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)

        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')

        self.wait_for_row_in_list_table('1: Купить вагонку')
        self.wait_for_row_in_list_table('2: Купить гвозди')

        # self.fail('Закончить тест!')

    # def test_can_start_a_list_for_one_user(self):
    #     """тест: можно начать список для одного пользователя"""
    #     self.wait_for_row_in_list_table('1: Купить вагонку')
    #     self.wait_for_row_in_list_table('2: Купить гвозди')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """тест: многочисленные пользователи могут начать списки по разным URL"""
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить вагонку')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить вагонку')

        # Эдит получает уникальный url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Фрэнсис посещает сайт

        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от Эдит не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Chrome(executable_path='C:\\Users\\Anton\\PythonPJ\\TDD\\chromedriver\\chromedriver.exe')

        # Фрэнсис посещает домашнюю старницу
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить вагонку', page_text)
        self.assertNotIn('Купить гвозди', page_text)

        # Фрэнсис начинает новый список, вводя новый элемент
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Фрэнсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Опять-таки, нет ни следа от списка Эдит
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить вагонку', page_text)
        self.assertIn('Купить молоко', page_text)




# if __name__ == '__main__':
#     unittest.main(warnings='ignore')


