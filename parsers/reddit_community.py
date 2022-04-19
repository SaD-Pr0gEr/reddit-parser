import time
from typing import Type

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver

from config.config import BASE_DIR, DATA_COLUMNS
from utils.downloader import PhotoManager
from utils.file_managers import ExcelManager
from utils.selenium_manager import SeleniumManager
from selenium.webdriver import Firefox


class RedditCommunityParser(SeleniumManager, ExcelManager, PhotoManager):
    """Класс для парсинга сообщества reddit"""

    def __init__(self, excel_coordinates: dict, driver_path: str, driver: Type[WebDriver] = Firefox,
                 headless: bool = False):
        super(RedditCommunityParser, self).__init__(driver_path, driver, headless)
        ExcelManager.__init__(self, excel_coordinates)
        self.page_save_directory = "pages"
        self.page_save_path = str(BASE_DIR / f"{self.page_save_directory}/data.html")

    @staticmethod
    def to_soup(content: [str, bytes]):
        """Метод для конвертирования контента в суп"""

        return BeautifulSoup(content, "html.parser")

    def get_and_save_page(self, url: str) -> None:
        """Метод для набора и сохранения страницы на файл"""

        self.default_driver.get(url)
        self.default_driver.refresh()
        time.sleep(5)
        self.scroll_down(800)
        time.sleep(3)
        self.scroll_up(800)
        time.sleep(5)
        self.get_directory_or_create(str(BASE_DIR / self.page_save_directory))
        self.save_file(self.page_save_path, "w", "utf-8", self.default_driver.page_source)
        self.close_and_quit()
        print("Страница сохранена! Переходим к парсингу данных")

    def read_and_to_soup(self) -> BeautifulSoup:
        """Метод для чтения файла и конвертации в суп"""

        return self.to_soup(self.read_file(self.page_save_path, "r", "utf-8"))

    @staticmethod
    def parse_links(soup: BeautifulSoup) -> list:
        """Метод парсинга данных с супа"""

        links_list = []
        links_container = soup.find("div", attrs={"class": "rpBJOHq2PR60pnwJlUyP0"})
        for links in links_container:
            links_dict = {}
            get_post_link = links.select("div.y8HYJ-y_lTUHkQIc1mdCq > a.SQnoC3ObvgnGjWt90zD9Z")
            if not get_post_link:
                continue
            links_dict["post_link"] = f"https://www.reddit.com{get_post_link[0]['href']}"
            get_photo_link = links.select(
                f"div._2FCtq-QzlfuN-SwVMUZMM3 + div.STit0dLageRsa2yR4te_b > div.m3aNC6yp8RrNM_-a0rrfa > "
                f"div._3JgI-GOrkmyIeDeyzXdyUD > div._1NSbknF8ucHV2abfCZw2Z1 > a > div > div > img"
            )
            if get_photo_link:
                links_dict["photo_link"] = get_photo_link[0]["src"]
            get_post_title = links.select("div._2SdHzo12ISmrC8H86TgSCp > h3._eYtD2XCVieq6emjKBH3m")
            if get_post_title:
                links_dict["post_title"] = get_post_title[0].text
            links_list.append(links_dict)
        if not links_list:
            return []
        print("Список данных(ссылка на пост, название поста, ссылка на фото) готов!")
        return links_list

    def insert_data(self, data_list: list, file_path: str) -> None:
        """Метод для сохранения данных"""

        row = 2
        for info in data_list:
            self.sheet[row][0].value = info["post_link"]
            self.sheet[row][1].value = info.get("photo_link", "")
            self.sheet[row][2].value = info.get("post_title", "")
            row += 1
        self.save_and_close(file_path)
        print(f"Данные успешно сохранены в excel по пути: {file_path}")

    def download_photos(self, photo_links_list: list, save_directory: str) -> None:
        """Метод скачивания фотографий"""

        self.get_directory_or_create(save_directory)
        for link in photo_links_list:
            photo_name = link.split('/')[-1]
            self.download_photo(link, f"{save_directory}/{photo_name}")
        print(f"Картинки успешно скачаны по пути: {save_directory}")


def runner():
    community_page = input(
        "Ссылка на страницу сообщества где новости отсотрированы по последнему: "
    ) or "https://www.reddit.com/r/AskElectronics/new/"
    get_excel_directory = input("Название папки для сохранения excel файлов: ").strip()
    excel_file_name = input("Название файла excel(без .xlsx): ").strip()
    photo_save_directory = input("Название папки для сохранения фото: ").strip()
    reddit_parser = RedditCommunityParser(DATA_COLUMNS, str(BASE_DIR / "drivers/geckodriver.exe"))
    reddit_parser.get_directory_or_create(str(BASE_DIR / get_excel_directory))
    reddit_parser.get_directory_or_create(str(BASE_DIR / photo_save_directory))
    reddit_parser.get_directory_or_create(str(BASE_DIR / reddit_parser.page_save_directory))
    reddit_parser.get_and_save_page(community_page)
    page_soup = reddit_parser.read_and_to_soup()
    photo_info_list = reddit_parser.parse_links(page_soup)
    reddit_parser.insert_data(photo_info_list, str(BASE_DIR / get_excel_directory / f"{excel_file_name}.xlsx"))
    for photo_info in photo_info_list:
        photo_link = photo_info.get("photo_link")
        if not photo_link:
            continue
        reddit_parser.download_photo(photo_link,
                                     str(BASE_DIR / photo_save_directory / photo_link.split("/")[-1].split("?")[0]))
    print("Фотографии скачаны!")


if __name__ == "__main__":
    runner()
