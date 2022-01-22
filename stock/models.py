from django.db import models

# Create your models here.

class Company(models.Model):
    code = models.CharField(max_length=20, primary_key=True) # 기업 코드
    company = models.CharField(max_length=40) # 회사명
    last_update = models.DateField() # 정보 업데이트 날짜

    def __str__(self):
        return self.company # 어드민 사이트 내 리스트에서 회사 명으로 리스트 보이기