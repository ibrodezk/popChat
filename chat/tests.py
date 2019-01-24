# chat/tests.py
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import time
class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True  # emulate StaticLiveServerTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            cd = '/usr/local/bin/chromedriver'
            chrome = '/usr/bin/google-chrome-stable'
            chrome_options = Options()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--no-sandbox')

            chrome_options.add_argument("--window-size=1920,1080");
            chrome_options.add_argument("--disable-gpu");
            chrome_options.add_argument("--disable-extensions");
            chrome_options.add_experimental_option("useAutomationExtension", False);
            chrome_options.add_argument("--proxy-server='direct://'");
            chrome_options.add_argument("--proxy-bypass-list=*");
            chrome_options.add_argument("--start-maximized");

            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")


            chrome_options.binary_location = chrome
            chrome_options.add_argument('--disable-dev-shm-usage')
            cls.driver = webdriver.Chrome(cd, chrome_options=chrome_options)
            # cls.driver = webdriver.Chrome(executable_path=cd, )
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_stress(self):
        try:
            start = 4
            end = 5
            rooms = [('room_' + str(x)) for x in range(start, end)]
            for ind in range(start, end):
                self._enter_chat_room('room_5')
                self._open_new_window()
            # time.sleep(30)
            self._switch_to_window(0)
            for ind in range(start, end):

                self._post_message('hello_' + str(ind))
                # self._switch_to_window(ind - 3)

            for ind in range(start, end):
                self._switch_to_window(ind - 4)
                for ind2 in range(start, end):
                    WebDriverWait(self.driver, 2).until(lambda _:
                        'hello_' + str(ind2) in self._chat_log_value,
                        'Message was not received by window ' + str(ind) + ' from window ' + str(ind2))
        finally:
            time.sleep(8)
            self._close_all_new_windows()

    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        try:
            self._enter_chat_room('room_0')

            self._open_new_window()
            self._enter_chat_room('room_0')
            time.sleep(1)
            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value,
                'Message was not received by window 1 from window 1')
            self._switch_to_window(1)
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value,
                'Message was not received by window 2 from window 1')
        finally:
            # time.sleep(10)
            self._close_all_new_windows()

    def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        try:
            self._enter_chat_room('room_1')

            self._open_new_window()
            self._enter_chat_room('room_2')
            time.sleep(1)
            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value,
                'Message was not received by window 1 from window 1')

            self._switch_to_window(1)
            self._post_message('world')

            WebDriverWait(self.driver, 2).until(lambda _:
                'world' in self._chat_log_value,
                'Message was not received by window 2 from window 2')
            self.assertTrue('hello' not in self._chat_log_value,
                'Message was improperly received by window 2 from window 1')
        finally:
            # time.sleep(10)
            self._close_all_new_windows()

    # === Utility ===

    def _enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + '/chat/')
        ActionChains(self.driver).send_keys(room_name + '\n').perform()
        WebDriverWait(self.driver, 2).until(lambda _:
            room_name in self.driver.current_url)

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to_window(self.driver.window_handles[0])

    def _switch_to_window(self, window_index):
        self.driver.switch_to_window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message + '\n').perform()

    @property
    def _chat_log_value(self):
        return self.driver.find_element_by_css_selector('#chat-log').get_property('value')
