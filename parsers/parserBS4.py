import requests
from bs4 import BeautifulSoup
from utils.file_managers import FileManager


class SoupConverter:
    """Класс для конвертации html в объект soup"""

    @staticmethod
    def convert(content):
        soup = BeautifulSoup(content, 'html.parser')
        return soup if soup else None


class ParsePostLinks:
    """Метод для парсинга ссылок на посты"""

    @staticmethod
    def parseLinks(soup: BeautifulSoup):
        postLinkList = []
        contentContainer = soup.find("div", attrs={"class": "rpBJOHq2PR60pnwJlUyP0"})
        for content in contentContainer:
            dataDict = {}
            getLink = content.select("div.y8HYJ-y_lTUHkQIc1mdCq > a.SQnoC3ObvgnGjWt90zD9Z")
            if getLink:
                postLink = f"https://www.reddit.com{getLink[0]['href']}"
                dataDict['link'] = postLink
                photoLink = content.select(
                    f"div._2FCtq-QzlfuN-SwVMUZMM3 + div.STit0dLageRsa2yR4te_b > div.m3aNC6yp8RrNM_-a0rrfa > div._3JgI-GOrkmyIeDeyzXdyUD > div._1NSbknF8ucHV2abfCZw2Z1 > a > div > div > img"
                )
                if photoLink:
                    link = photoLink[0]['src']
                    dataDict['photoLink'] = link
                getHeader = content.select("div._2SdHzo12ISmrC8H86TgSCp > h3._eYtD2XCVieq6emjKBH3m")
                if getHeader:
                    postHeader = getHeader[0].text
                    dataDict['title'] = postHeader
            if dataDict:
                postLinkList.append(dataDict)
        print("Список данных(ссылка на пост, название поста, ссылка на фото) готов!")
        return postLinkList if postLinkList else None


if __name__ == "__main__":
    man = FileManager().reader('../pages/first.html', 'r', 'utf-8')
    soup2 = SoupConverter().convert(man)
    links = ParsePostLinks().parseLinks(soup2)
