import re
from .mainnews import MainNews

URLS_AMERICAN = {
    'AP_News': 'https://apnews.com/hub/ap-top-news',
    'ABC_News': 'https://abcnews.go.com',
    'FOX_News': 'https://www.foxnews.com',
}

URLS_RUSSIAN = {
    'RT_news': 'https://www.rt.com',
    'Sputnik_news': 'https://sputniknews.com',
    'Moscow_times': 'https://www.themoscowtimes.com/news',
}

URLS_CHINESE = {
    'News_CN': 'https://english.news.cn/world/index.htm',
    'CGTN_news': 'https://www.cgtn.com',
    'Global_times_news': 'https://www.globaltimes.cn/world/index.html',
}

URLS_EUROPEAN = {
    'BBC_news': 'https://www.bbc.com/news/world',
    'Euronews': 'https://www.euronews.com/programs/world',
    'Politico': 'https://www.politico.eu',
    'Financial_times': 'https://www.ft.com/world'
}


class AmericanNews(MainNews):
    def __init__(self, urls=URLS_AMERICAN):
        super().__init__(urls=urls)
        self.parsing_urls([self.parse_ap_News, self.parse_FOX_News, self.parse_abc_News])

    def parse_ap_News(self):
        data = self.parsing(n_url='AP_News')
        if data == 'Error':
            return
        news_blocks = data.find(name='div', class_='Body').findAll(attrs={'data-key': re.compile('story-link')})
        news_ap = [{'source': 'The Associated Press',
                    'link': f"https://apnews.com{el['href']}",
                    'text': el.find('p').text} for el in news_blocks]
        self.all_news.append(news_ap)

    def parse_abc_News(self):
        data = self.parsing(n_url='ABC_News')
        if data == 'Error':
            return
        news_blocks = data.find(class_='ContentList').findAll('a')
        news_abc = [{'source': 'ABC news',
                     'link': el['href'],
                     'text': el.find('h2').text} for el in news_blocks]
        self.all_news.append(news_abc)

    def parse_FOX_News(self):
        data = self.parsing(n_url='FOX_News')
        if data == 'Error':
            return
        news_blocks = data.find(class_='collection collection-article-list').findAll('h2')
        news_fox = [{'source': 'FOX news',
                     'link': el.find('a')['href'],
                     'text': el.text} for el in news_blocks]
        self.all_news.append(news_fox)


class RussianNews(MainNews):
    def __init__(self, urls=URLS_RUSSIAN):
        super().__init__(urls=urls)
        self.parsing_urls([self.parse_rt_news, self.parse_sputnik_news, self.parse_moscow_times], amount_news=5)

    def parse_rt_news(self):
        data = self.parsing(n_url='RT_news')
        if data == 'Error':
            return
        news_blocks = data.findAll('a', class_='main-promobox__link')
        news_rt = [{'source': 'RT news',
                    'link': f"https://www.rt.com{el['href']}",
                    'text': el.text.strip()} for el in news_blocks]
        self.all_news.append(news_rt)

    def parse_sputnik_news(self):
        data = self.parsing(n_url='Sputnik_news')
        if data == 'Error':
            return
        news_block = data.findAll('div', class_='floor__cell-shape')
        news_sputnik = [{
            'source': 'Sputnik news',
            'link': f"https://sputniknews.com{el.find('a')['href']}",
            'text': el.find('span').text
        } for el in news_block]
        self.all_news.append(news_sputnik)

    def parse_moscow_times(self):
        data = self.parsing(n_url='Moscow_times')
        if data == 'Error':
            return
        news_blocks = data.find('ul', class_='listed-articles').findAll('a')
        news_moscowtimes = [{
            'source': 'The Moscow times',
            'link': el['href'],
            'text': el.find('h5').text.strip()} for el in news_blocks]
        self.all_news.append(news_moscowtimes)


class ChineseNews(MainNews):
    def __init__(self, urls=URLS_CHINESE):
        super().__init__(urls=urls)
        self.parsing_urls([self.parse_cn_news, self.parse_cgtn_news, self.parse_glob_times_news])

    def parse_cn_news(self):
        data = self.parsing(n_url='News_CN')
        if data == 'Error':
            return
        news_blocks = data.find('div', class_='part01').findAll('a')[1:]
        news_cn = [{'source': 'CN news',
                    'link': el['href'].lstrip('.'),
                    'text': el.text} for el in news_blocks]
        for news in news_cn:
            if not news['link'].startswith('https://'):
                news['link'] = f"https://english.news.cn{news['link']}"
        self.all_news.append(news_cn)

    def parse_cgtn_news(self):
        data = self.parsing(n_url='CGTN_news')
        if data == 'Error':
            return
        news_blocks = data.find('div', class_='live-blog-area').findAll('a')[1:]
        news_cgtn = [{'source': 'CGTN news',
                      'link': el['href'],
                      'text': el.text.strip()} for el in news_blocks]
        self.all_news.append(news_cgtn)

    def parse_glob_times_news(self):
        data = self.parsing(n_url='Global_times_news')
        if data == 'Error':
            return
        news_blocks = data.find('div', class_='level01_list').findAll('a', class_='new_title_ms')
        news_glob_news = [{'source': 'GT news',
                           'link': el['href'],
                           'text': el.text.strip()} for el in news_blocks]
        self.all_news.append(news_glob_news)


class EuropeanNews(MainNews):
    def __init__(self, urls=URLS_EUROPEAN):
        super().__init__(urls=urls)
        self.parsing_urls([self.parse_bbc_news, self.parse_euronews, self.parse_politico, self.parse_ft])

    def parse_bbc_news(self):
        data = self.parsing(n_url='BBC_news')
        if data == 'Error':
            return
        news_blocks = data.find('div', class_='gel-layout gel-layout--equal').findAll('a', class_='gs-c-promo-heading')
        news_bbc = [{'source': 'BBC news',
                     'link': f"https://www.bbc.com{el['href']}",
                     'text': el.text} for el in news_blocks]
        self.all_news.append(news_bbc)

    def parse_euronews(self, amount_news=6):
        data = self.parsing(n_url='Euronews')
        if data == 'Error':
            return
        news_blocks = data.find('div', class_='o-block-listing__articles').findAll('a', attrs={'rel': 'bookmark'})[:amount_news]
        news_euronews = [{'source': 'Euronews',
                          'link': f"https://www.euronews.com{el['href']}",
                          'text': el.text.strip()} for el in news_blocks]
        self.all_news.append(news_euronews)

    def parse_politico(self):
        data = self.parsing(n_url='Politico')
        if data == 'Error':
            return
        news_blocks = data.find('div', class_='content-listing__content grid grid__columns--1').findAll('div', class_='card card__layout--default')
        news_politico = [{'source': 'Politico',
                          'link': el.find('a')['href'],
                          'text': el.find('a').text.strip()} for el in news_blocks]
        self.all_news.append(news_politico)

    def parse_ft(self):
        data = self.parsing(n_url='Financial_times')
        if data == 'Error':
            return
        news_blocks = data.find('div',
                                class_='o-teaser-collection',
                                attrs={'data-trackable': "top-stories-column-one"}).findAll('a', class_='js-teaser-heading-link')
        news_ft = [{'source': 'Financial Times',
                    'link': f"https://ft.com/content{el['href']}",
                    'text': el.text.strip()} for el in news_blocks]
        self.all_news.append(news_ft)




