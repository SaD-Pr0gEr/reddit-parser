import random

import requests
from requests import Response


class RequestManager:
    """Менеджер работы с requests"""

    user_agents_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61"
    ]

    def get_url_search_rubric(self, search_rubric: str, delimiter: str) -> None:
        """Метод для получения нужной URL"""
        pass

    def get(self, url: str, headers: dict = None, **kwargs) -> Response:
        """Метод для get запроса"""

        if headers:
            headers['User-Agent'] = random.choice(self.user_agents_list)
        else:
            headers = {
                "User-Agent": random.choice(self.user_agents_list)
            }
        return requests.get(url, headers=headers, **kwargs)

    def post(self, url: str, headers: dict = None, **kwargs) -> Response:
        """Метод для post запроса"""

        if headers:
            headers['User-Agent'] = random.choice(self.user_agents_list)
        else:
            headers = {
                "User-Agent": random.choice(self.user_agents_list)
            }
        return requests.post(url, headers=headers, **kwargs)

    def put(self, url: str, headers: dict = None, **kwargs) -> Response:
        """Метод для put запроса"""

        if headers:
            headers['User-Agent'] = random.choice(self.user_agents_list)
        else:
            headers = {
                "User-Agent": random.choice(self.user_agents_list)
            }
        return requests.put(url, headers=headers, **kwargs)

    def patch(self, url: str, headers: dict = None, **kwargs) -> Response:
        """Метод для patch запроса"""

        if headers:
            headers['User-Agent'] = random.choice(self.user_agents_list)
        else:
            headers = {
                "User-Agent": random.choice(self.user_agents_list)
            }
        return requests.patch(url, headers=headers, **kwargs)
