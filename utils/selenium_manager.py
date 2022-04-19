import random
from typing import Type

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver


class SeleniumManager:
    """Менеджер работы с selenium(по дефолту для Firefox)"""

    user_agents_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61"
    ]

    def __init__(self, driver_path: str, driver: Type[WebDriver] = webdriver.Firefox, headless: bool = False) -> None:
        self.default_driver = None
        self.configure_browser(driver_path, driver, headless)

    def configure_browser(self, driver_path: str, driver: Type[WebDriver] = webdriver.Firefox,
                          headless: bool = False) -> None:
        """Конфигуриация браузера. Надо переопределить для других видов браузера!"""

        default_options = webdriver.FirefoxOptions()
        default_options.set_preference('general.useragent.override', random.choice(self.user_agents_list))
        default_options.set_preference("dom.webdriver.enabled", False)
        default_options.headless = headless
        self.default_driver = driver(options=default_options,
                                     executable_path=driver_path)
        print("Браузер скорфигурирован!")

    def scroll_down(self, down_counter: int) -> None:
        for i in range(down_counter):
            self.default_driver.find_element_by_tag_name("html").send_keys(Keys.DOWN)

    def scroll_up(self, up_counter: int) -> None:
        for i in range(up_counter):
            self.default_driver.find_element_by_tag_name("html").send_keys(Keys.DOWN)

    def close_and_quit(self) -> None:
        """Метод для выхода с браузера и остановки в процессах"""

        self.default_driver.close()
        self.default_driver.quit()
        print("Браузер успешно остановлен!")
