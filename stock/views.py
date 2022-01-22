from django.shortcuts import render
from django.http import HttpResponse # 페이지 요청에 대한 응답 시 사용하는 클래스
from .models import Company

# def index(request):
#     return HttpResponse("안녕하세요. 기본 페이지 입니다.")

def index(request):
    #edit
    company_list = Company.objects.all()		# Company 모델에 있는 정보를 전부 가져온다.
    context = {'company_list': company_list}	# company_list의 정보를 context에 담는다.

    return render(request, 'stock/index.html', context)