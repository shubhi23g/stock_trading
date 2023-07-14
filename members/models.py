from django.db import models
class CompanyList(models.Model) :
    name = models.CharField(max_length=100)

class StockTrading(models.Model):
    company=models.CharField(max_length=100)
    closing_prize=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateField()
    class Meta:
        db_table = 'stock_trading'
        unique_together = ('company', 'date')

class UserProfile(models.Model):
    company_name=models.CharField(max_length=100)
    stock_prize=models.DecimalField(max_digits=10,decimal_places=2)
    buying_date=models.DateField()
    class Meta:
        unique_together = ('company_name', 'buying_date')
    
