from django.db import models

# Create your models here.


class Company(models.Model):
    code = models.CharField(max_length=20, primary_key=True)  # 기업 코드
    company = models.CharField(max_length=40)  # 회사명
    last_update = models.DateField()  # 정보 업데이트 날짜

    def __str__(self):
        return self.company  # 어드민 사이트 내 리스트에서 회사 명으로 리스트 보이기


class StockDaily(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    company = models.CharField(max_length=40, blank=True, null=True)
    date = models.DateField()
    open = models.BigIntegerField(blank=True, null=True)
    high = models.BigIntegerField(blank=True, null=True)
    low = models.BigIntegerField(blank=True, null=True)
    close = models.BigIntegerField(blank=True, null=True)
    diff = models.BigIntegerField(blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_daily'
        unique_together = (('code', 'date'),)

    def __str__(self):
        rst = {
            'code': self.code,
            'company': self.company,
            'date': self.date,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'diff': self.diff,
            'volume': self.volume
        }
        return rst
