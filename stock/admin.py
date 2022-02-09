from django.contrib import admin
from .models import *

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['company']  # 회사명으로 검색


# 쉘에서 하던 작업을 어드민 페이지에서 더 편하게 할 수 있다.
admin.site.register(Company, CompanyAdmin)


class PriceAdmin(admin.ModelAdmin):
    search_fields = ['company']  # 회사명으로 검색


admin.site.register(StockDaily, PriceAdmin)
