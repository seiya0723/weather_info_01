from django.shortcuts import render
from django.views import View

from .models import Weather

from .forms import YearMonthForm


class IndexView(View):

    def get(self, request, *args, **kwargs):

        context = {}

        #ページ上部に最新の天気を数件表示させる
        #context["weather"]  = Weather.objects.order_by("-dt").first()
        context["weathers"] = Weather.objects.order_by("-dt")[:3]

        #ここで年月検索を行う。パラメーターの値をバリデーション、未指定もしくは間違った値が指定されている場合、全て表示させる。
        form    = YearMonthForm(request.GET)
        if form.is_valid():
            cleaned         = form.clean()
            all_weathers    = Weather.objects.filter(dt__year=cleaned["year"],dt__month=cleaned["month"]).order_by("-dt")
        else:
            all_weathers    = Weather.objects.order_by("-dt")


        #TODO:ここでページネーションを実装する。ただし、検索機能とページ移動を両立させなければならない。
        #https://noauto-nolife.com/post/django-paginator/
        context["all_weathers"] = all_weathers


        #年月入力のための最古と最新データを抜き取り、年月のリストを作る。
        oldest_dt   = Weather.objects.order_by("dt").first().dt
        newest_dt   = Weather.objects.order_by("-dt").first().dt

        oldest_year = oldest_dt.year
        newest_year = newest_dt.year
        print(oldest_year)
        print(newest_year)
        
        years   = []
        for i in range(newest_year,oldest_year-1,-1):
            years.append(i)

        context["years"]    = years

        #リストの内包表記
        #https://note.nkmk.me/python-list-comprehension/
        context["months"]   = [ i for i in range(1,13) ]

        return render(request,"tenki/index.html",context)

index   = IndexView.as_view()
