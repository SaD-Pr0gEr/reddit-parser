from parsers.parserBS4 import ParsePostLinks, RequestSender
from parsers.parserSelenium import RedditParser
from utils.downloader import PhotoDownloader
from utils.file_managers import ExcelManager


class Runner(RedditParser, ParsePostLinks):
    """Класс для запуска парсера"""

    def __init__(self, initedExcelManager: ExcelManager, classPhotoDownloader, initedRequestSender: RequestSender):
        super().__init__()
        self.dataList = None
        self.run(initedExcelManager, classPhotoDownloader, initedRequestSender)

    def run(self, initedExcelManager: ExcelManager, classPhotoDownloader: PhotoDownloader, initedRequestSender: RequestSender):
        companyPage = 'https://www.reddit.com/r/AskElectronics/new/'
        self.checkFilePath('./pages')
        self.checkFilePath('./drivers')
        self.checkFilePath('./data')
        self.checkFilePath('./photos')
        htmlPath = "./pages/data.html"
        self.getPage(companyPage, htmlPath, 'utf-8')
        soup = self.parseData(htmlPath, 'r', 'utf-8')
        self.dataList = self.parseLinks(soup)
        fileNameExcel = input('Вводите название excel файла(на латинице): ')
        urlList = (urls.get('photoLink') for urls in self.dataList)
        initedExcelManager.insertData(self.dataList, './data', fileNameExcel)
        classPhotoDownloader.download(self, './photos', urlList, initedRequestSender)
        print("Данные сохранены и скачаны успешно! Программа завершила работу!")


if __name__ == "__main__":
    columns = {
        "A1": "Ссылка на пост",
        "B1": "Ссылка на фото",
        "C1": "Название поста"
    }
    Runner(ExcelManager(columns), PhotoDownloader, RequestSender())
