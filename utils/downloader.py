import urllib3
from PIL import Image
from urllib3.exceptions import InsecureRequestWarning

from utils.file_managers import FileManager
from utils.request_manager import RequestManager


class PhotoManager(RequestManager, FileManager):
    """Загрузчик фото"""

    def download_photo(self, link: str, file_path: str, headers: dict = None, verify: bool = False) -> None:
        """Метод для скачивания и сохранения фото"""

        urllib3.disable_warnings(InsecureRequestWarning)
        self.save_byte_file(file_path, self.get(link, headers=headers, verify=verify).content)

    @staticmethod
    def get_photo_sizes(photo_path: str):
        """Метод который вернёт ширину и высоту фото"""

        with Image.open(photo_path) as img:
            width, height = img.size
        return width, height
