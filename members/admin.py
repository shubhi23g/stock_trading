from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
# class FileAdmin(admin.ModelAdmin):
#     list_display = ["id", "company", "closing_prize", "date"]
admin.site.register(StockTrading)