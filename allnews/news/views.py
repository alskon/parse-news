from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .api import news

COLORS = ['#FBE8A6', '#F4976C', '#B4DFE5', '#D2FDFF']
refresh_time = 60
TIME_RANGE = [0, 30, 60, 120, 240, 360]
# Create your views here.


class MainPage(View):

    def __init__(self):
        super(MainPage, self).__init__()
        self.time_range = TIME_RANGE
        self.refresh_time = refresh_time
        print(self.refresh_time)

    def get(self, request, num_blocks=4):
        american_news = news.AmericanNews()
        russian_news = news.RussianNews()
        chinese_news = news.ChineseNews()
        european_news = news.EuropeanNews()

        return render(request, 'news/main.html', {
            'num_blocks': num_blocks,
            'american_news': american_news.block_news,
            'russian_news': russian_news.block_news,
            'chinese_news': chinese_news.block_news,
            'european_news': european_news.block_news,
            'colors': COLORS,
            'refresh_time': self.refresh_time,
            'time_range': self.time_range,
        })

    def post(self, request):
        global refresh_time
        new_time = request.POST.get('time')
        new_time = int(new_time)
        refresh_time = new_time
        print(new_time)
        print(self.refresh_time)
        return HttpResponseRedirect(redirect_to='/')
