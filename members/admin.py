from django.contrib import admin
from .models import CompanyList,StockTrading,UserProfile
# Register your models here.
admin.site.register(CompanyList)
# admin.site.register(StockTrading)
admin.site.register(UserProfile)
class FileAdmin(admin.ModelAdmin):
    list_display = ["id", "company", "closing_prize", "date"]
admin.site.register(StockTrading, FileAdmin)