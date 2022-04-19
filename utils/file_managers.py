import os

from openpyxl import Workbook


class FileManager:
    """Файловый менеджер"""

    @staticmethod
    def get_directory_or_create(directory_path: str) -> None:
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

    @staticmethod
    def save_file(file_path: str, write_mode: str, encoding: str, content: str):
        with open(file_path, write_mode, encoding=encoding) as file:
            file.write(content)

    @staticmethod
    def save_byte_file(file_path: str, content: bytes):
        with open(file_path, "wb") as file:
            file.write(content)

    @staticmethod
    def read_file(file_path: str, read_mode: str, encoding: str):
        with open(file_path, read_mode, encoding=encoding) as file:
            read = file.read()
        return read


class ExcelManager(Workbook):
    """Менеджер работы с excel"""

    def __init__(self, coordinates: dict) -> None:
        super(ExcelManager, self).__init__()
        self.sheet = self.active
        self.__configure_columns(coordinates)

    def __configure_columns(self, coordinates: dict) -> None:
        """Метод для конфигуриации ячеек"""

        for column, value in coordinates.items():
            self.sheet[column] = value

    def insert_data(self, data_list: str, file_path: str) -> None:
        """Метод добавления данных"""
        pass

    def save_and_close(self, file_path: str) -> None:
        """Метод для сохранения и выхода с файла"""

        self.save(file_path)
        self.close()
