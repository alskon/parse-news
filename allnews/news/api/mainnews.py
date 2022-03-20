import requests
from bs4 import BeautifulSoup


class MainNews:
    def __init__(self, urls):
        self.urls = urls
        self.all_news = []
        self.block_news = []

    def parsing(self, n_url: str):
        try:
            headers = {"user-agent": "Mozilla/5.0"}
            data = requests.get(self.urls[n_url], headers=headers).text
            data = BeautifulSoup(data, features='html.parser')
        except:
            data = 'Error'
            return data
        return data

    def compose_news(self, amount_news: int = 3):
        self.all_news = [value for value in self.all_news if value]
        for block in self.all_news:
            if len(block) < amount_news:
                amount_news = len(block)
        block_news = []
        for i in range(amount_news):
            block_news.append([news[i] for news in self.all_news])
            self.block_news = [item for block in block_news for item in block]

    def parsing_urls(self, funcs, *args, **kwargs):
        for func in funcs:
            func()
        self.compose_news(*args, **kwargs)
