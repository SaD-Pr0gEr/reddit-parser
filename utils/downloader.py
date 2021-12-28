from parsers.parserBS4 import RequestSender
from utils.file_managers import FileManager
import datetime


class PhotoDownloader:
    """Класс для загрузки фото"""

    @staticmethod
    def download(saveClass: FileManager, path, urlList, initedRequestSender: RequestSender):
        """Метод для загрузки фото"""

        for url in urlList:
            if url:
                photoFormat = saveClass.fileFormatFromUrl(url)
                photoName = saveClass.fileNameFromUrl(url)
                response = initedRequestSender.get(url)
                BasePath = f"{path}/{str(datetime.datetime.today()).split(' ')[0]}"
                saveClass.checkFilePath(BasePath)
                saveClass.save(
                    f"{BasePath}/{photoName}.{photoFormat}",
                    None,
                    "wb",
                    response.content
                )
        print("Фото сохранено успешно!")
        return True


if __name__ == "__main__":
    d = PhotoDownloader()
    d.download(
        FileManager(),
        '../photos',
        ["https://preview.redd.it/c1dexb6xg6881.jpg?width=640&crop=smart&auto=webp&s=8a84e5092d8490f6c1130c54f925bf2d026e13e0"],
        RequestSender()
    )
