from django.conf import Settings
from django.shortcuts import render
from django.http import HttpResponse  # 페이지 요청에 대한 응답 시 사용하는 클래스
from django.conf import settings
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
import requests  # 네이버 뉴스 정보 크롤링
from bs4 import BeautifulSoup


def index(request):
    # edit
    company_list = Company.objects.all()
    context = {'company_list': company_list}

    return render(request, 'stock/index.html', context)


def dashboard(request):

    if request.method == 'GET':
        # 뉴스 타이틀, 콘텐츠 가져오기 - 크롤링 1
        url1 = f'http://finance.naver.com/news/mainnews.naver'

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        response2 = requests.get(url1, headers=headers)
        soup = BeautifulSoup(response2.text, 'html.parser')

        news_title = soup.select(
            '#contentarea_left > div.mainNewsList > ul > li:nth-child(1) > dl > dd.articleSubject > a')
        news_content = soup.select(
            '#contentarea_left > div.mainNewsList > ul > li:nth-child(1) > dl > dd.articleSummary')
        news_image = soup.select(
            '#contentarea_left > div.mainNewsList > ul > li:nth-child(1) > dl > dt > a > img')

        context = dict()

        news_link = 'http://finance.naver.com/' + news_title[0].get('href')
        news_title = news_title[0].text

        # 뉴스 이미지 추출 작업 - 크롤링 2
        url2 = news_link

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        response2 = requests.get(url2, headers=headers)
        soup = BeautifulSoup(response2.text, 'html.parser')
        news_image = soup.select('#content > span > img')[0].get('src')

        # 뉴스 요약 내용 정제
        news_content = news_content[0].text.lstrip()

        news_contents = ''
        print(news_content)
        for nc in news_content:
            if nc == '\n':
                break
            elif nc == '\t':
                continue
            news_contents += nc

        main_news = {
            'news_title': news_title,
            'news_link': news_link,
            'news_content': news_contents,
            'news_image': news_image
        }

        context = {
            'main_news': main_news
        }
        print(context)
        return render(request, 'stock/dashboard.html', context=context)

    # company_list = Company.objects.all()
    # context = {'company_list': company_list}
    # return render(request, 'stock/dashboard.html', context)


def company(request):
    comp = Company.objects.all()
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    # 조회
    company_list = comp.order_by('company')
    if kw:
        company_list = company_list.filter(
            Q(code__icontains=kw) |
            Q(company__icontains=kw)
        ).distinct()

    # 페이징처리
    paginator = Paginator(company_list, 20)
    page_obj = paginator.get_page(page)
    context = {'comp': page_obj, 'page': page, 'kw': kw}
    return render(request, 'stock/company.html', context)


def daily(request):
    queryset = StockDaily.objects.all()
    # queryset을 통하여 별도로 SQL을 작성할 필요 없이 DB로 부터 데이터를 가져오고 추가, 수정, 삭제가 가능
    if not 'kw' in request.GET:
        daily = queryset.filter(company='삼성전자')
        daily = daily.order_by('-date')
    else:  # code, company 명으로 전달될 경우
        kw = request.GET['kw']
        daily = queryset.filter(code=kw)
        daily = daily.order_by('-date')
        if not daily:
            daily = queryset.filter(company=kw)
            daily = daily.order_by('-date')
    if not daily:
        daily = False
    context = {'daily': daily}
    return render(request, 'stock/daily.html', context)


# 네이버 검색 API 활용 (Date:2022.02.06)
# def search(request):
#     if request.method == 'GET':
#         config_secret_debug = json.loads(
#             open(settings.SECRET_DEBUG_FILE).read())
#         # getattr(
#         #     settings, 'SECRET_DEBUG_FILE', None)

#         client_id = config_secret_debug['NAVER']['CLIENT_ID']
#         client_secret = config_secret_debug['NAVER']['CLIENT_SECRET']

#         q = request.GET.get('q')
#         encText = urllib.parse.quote("주가".format(q))
#         url = "https://openapi.naver.com/v1/search/news?query=" + encText  # json 결과
#         news_api_request = urllib.request.Request(url)
#         news_api_request.add_header("X-Naver-Client-Id", client_id)
#         news_api_request.add_header("X-Naver-Client-Secret", client_secret)
#         response = urllib.request.urlopen(news_api_request)
#         rescode = response.getcode()
#         if (rescode == 200):
#             response_body = response.read()
#             print(response_body.decode('utf-8'))
#             result = json.loads(response_body.decode('utf-8'))
#             items = result.get('items')

#             context = {
#                 'items': items
#             }
#         return render(request, 'stock/search.html', context=context)


# 네이버 경제 메인
def news(request):
    if request.method == 'GET':
        # 오늘의 경제 용어
        url1 = f'https://www.mk.co.kr/dic/'

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        response1 = requests.get(url1, headers=headers)
        soup = BeautifulSoup(response1.text, 'html.parser')

        kor_word = soup.select(
            '#container > div.today_wrap > div.today_word > h4')
        eng_word = soup.select(
            '#container > div.today_wrap > div.today_word > span')
        word_content = soup.select('#area_content')
        today = {
            'k_word': kor_word[0].text.strip(),
            'e_word': eng_word[0].text.strip(),
            'w_content': word_content[0].text.strip()
        }

        # 네이버 경제 메인
        url2 = f'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        response2 = requests.get(url2, headers=headers)
        soup = BeautifulSoup(response2.text, 'html.parser')

        my_news = soup.select(
            '#main_content > div > div._persist > div:nth-child(1) > div.cluster_group._cluster_content > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a')
        my_news_content = soup.select(
            '#main_content > div > div._persist > div:nth-child(1) > div.cluster_group._cluster_content > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > div.cluster_text_lede')
        my_news_writing = soup.select(
            '#main_content > div > div._persist > div:nth-child(1) > div.cluster_group._cluster_content > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > div.cluster_text_info > div')
        my_news_image = soup.select(
            '#main_content > div > div._persist > div:nth-child(1) > div.cluster_group._cluster_content > div.cluster_body > ul > li:nth-child(1) > div.cluster_thumb > div.cluster_thumb_inner > a > img')
        my_news_date = soup.select(
            '#main_content > div > div._persist > div:nth-child(1) > div.cluster_group._cluster_content > div.cluster_head > div.cluster_head_inner > a'
        )

        newslist = list()
        nnews = list()
        context = dict()

        for news in my_news:  # 뉴스 제목을 리스트에 append
            nnews.append(news.text.strip())

        for i in range(len(nnews)):
            title = my_news[i].text.strip()
            link = my_news[i].get('href')
            content = my_news_content[i].text.strip()
            writing = my_news_writing[i].text.strip()
            date_ = my_news_date[i].get('href')
            date = date_[33:37]+'년 ' + date_[37:39]+'월 ' + date_[39:41]+'일'
            try:  # list index out of range 방지를 위한 예외처리
                image_s = my_news_image[i].get('src')
                image = my_news_image[i].get('src').replace(
                    'nf132_90', 'w647')  # 크기 조정을 위한 replace
            except:
                image_s = "NO IMAGE"
                image = "NO IMAGE"

            item_obj = {
                'title': title,
                'link': link,
                'content': content,
                'writing': writing,
                'image': image,
                'image_s': image_s,
                'date': date,
            }

            newslist.append(item_obj)
        context = {
            'items': newslist,
            'today_word': today
        }
        print(context)
        return render(request, 'stock/news.html', context=context)
