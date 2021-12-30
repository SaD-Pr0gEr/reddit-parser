import os
from datetime import datetime
import openpyxl as excel


class FileManager:
    """Класс файловый менеджер"""

    @staticmethod
    def reader(filePath, mode, encoding):
        """Метод для чтение файла"""

        with open(filePath, mode, encoding=encoding) as file:
            read = file.read()
            return read

    @staticmethod
    def save(filePath, encoding, mode, content):
        """Метод для сохранение файла"""

        if mode == "w":
            with open(filePath, mode, encoding=encoding) as file:
                file.write(content)
        else:
            with open(filePath, mode) as file:
                file.write(content)
        return filePath

    @staticmethod
    def fileFormatFromUrl(url: str):
        fileFormat = url.split("?")[0].split('/')[-1].split('.')[-1]
        return fileFormat

    @staticmethod
    def fileNameFromUrl(url: str):
        fileName = url.split("?")[0].split('/')[-1].split('.')[0]
        return fileName

    @staticmethod
    def checkFilePath(filePath):
        """Метод для проверки пути для файла excel"""

        if not os.path.exists(filePath):
            os.mkdir(filePath)


class ExcelManager(FileManager):
    """Менеджер для работы с excel файлами"""

    def __init__(self, colCoordinates: dict):
        self.book = excel.Workbook()
        self.sheet = self.book.active
        self.__configureColumns(colCoordinates)

    def __configureColumns(self, params: dict):
        """Метод для конфигуриации столбцов"""

        for column, value in params.items():
            self.sheet[column] = value

    def insertData(self, dataList: list, filePath, fileName):
        """Метод для добавления данных"""

        row = 2
        for data in dataList:
            try:
                self.sheet[row][0].value = data['link']
                self.sheet[row][1].value = data['photoLink']
                self.sheet[row][2].value = data['title']
            except Exception as e:
                self.sheet[row][0].value = data['link']
                self.sheet[row][2].value = data['title']
            row += 1
        self.checkFilePath(filePath)
        self.__saveAndClose(filePath, fileName)
        print("Данные успешно записаны!")

    def __saveAndClose(self, filePath, fileName):
        """Метод для сохранения файла"""

        Path = f"{filePath}/{fileName.replace(' ', '-')}-{str(datetime.today()).replace(' ', '-').replace(':', '-').replace('.', '-')}"
        self.book.save(f"{Path}.xlsx")
        self.book.close()
        print(f"Файл сохранён. \n Путь до файла: {Path}.xlsx")


if __name__ == "__main__":
    manager = FileManager().fileFormatFromUrl("https://preview.redd.it/mftffghp47881.jpg?width=320&crop=smart&auto=webp&s=04f4e362c4ea0441c137bb933b13967b26319970")
    manager2 = FileManager().fileNameFromUrl("https://preview.redd.it/wz8jo3qp47881.jpg?width=320&crop=smart&auto=webp&s=967d6fedad0e9fd1734838400755ba212a07c913")

    excelManager = ExcelManager({"A1": "test", "B1": "test2"})
    excelManager.insertData([{"test": "test", 'test2': "test2"}], '../data', "test")
