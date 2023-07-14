from rest_framework import serializers
from .models import *



class StockTradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTrading
        fields = '__all__' 