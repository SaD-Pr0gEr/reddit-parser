import random
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from parsers.parserBS4 import SoupConverter
from utils.file_managers import FileManager


class SeleniumConf(FileManager):
    """Класс для конфигуриации Selenium"""

    userAgentList = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    ]

    def __init__(self):
        self.Driver = None
        self.__configureBrowser()

    def __configureBrowser(self):
        """Метод для настройки браузера"""

        options = webdriver.FirefoxOptions()
        options.set_preference('general.useragent.override', random.choice(self.userAgentList))
        options.set_preference("dom.webdriver.enabled", False)
        options.headless = True
        self.Driver = webdriver.Firefox(
            options=options
        )
        print("Браузер сконфигурирован! ")


class RedditParser(SeleniumConf, SoupConverter, FileManager):
    """Класс для парсинга постов с Reddit"""

    def __init__(self):
        super().__init__()

    def getPage(self, url, filePath, encoding):
        """Метод чтобы открыть определённую страницу и сохранить её"""

        self.Driver.get(url)
        time.sleep(5)
        htmlPage = self.Driver.find_element(By.TAG_NAME, 'html')
        for i in range(500):
            htmlPage.send_keys(Keys.DOWN)
        time.sleep(15)
        self.save(filePath, encoding, "w", self.Driver.page_source)
        self.closeAndQuit()
        print(f"Страница сохранена в файл {filePath}")

    def parseData(self, filePath, mode, encoding):
        """Метод для преобразования файла в soup"""

        readContent = self.reader(filePath, mode, encoding)
        soup = self.convert(readContent)
        return soup

    def closeAndQuit(self):
        """Метод чтобы закрыть браузер"""

        self.Driver.close()
        self.Driver.quit()
        print("Браузер успешно закрыт!")


if __name__ == "__main__":
    parser = RedditParser()
    parser.getPage("https://www.reddit.com/r/AskElectronics/new/", "../pages/first.html", 'utf-8')
