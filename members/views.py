from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from datetime import datetime
import csv
import statistics
from dateutil.parser import parse as parse_date
from decimal import Decimal

@api_view(['POST'])
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        # Process the CSV file
        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
        # Skip the header row if necessary
        next(csv_data, None)
        # Process each row and save the stock prices
        for row in csv_data:
            date = parse_date(row[1])
            company_name = row[2]
            price = row[3]
            if (not StockTrading.objects.filter(company=company_name,date=date,closing_prize=price)) :
                StockTrading.objects.create(company=company_name,date=date,closing_prize=price)
            StockTrading.objects.values().order_by('date')
        return Response({"status": "success"})
    return Response({"status": "failed"})    


@api_view(['GET'])
def stock_result(request):
    company_name = request.data.get('company_name')    
    start_date = parse_date(request.data.get('start_date'))
    end_date = parse_date(request.data.get('end_date'))
    stock_prices = StockTrading.objects.filter(company__icontains=company_name, date__range=(start_date, end_date)).values().order_by('date')
    count = stock_prices.count()
    data1 = StockTradingSerializer(stock_prices, many=True, context={'request': request}).data
    buy_date,selling_date,buying_price,selling_price, max_profit,mean_stock_price,standard_deviation=result(stock_prices,count)
    return Response ({"message":data1,
                      "buy_date":buy_date,
                      "selling_date":selling_date,
                      "max_profit":max_profit,
                      "mean_stock_price":mean_stock_price,
                      "standard_deviation":standard_deviation,
                      "buying_price":buying_price,
                      "selling_price":selling_price})


def result(stock_prices,count,buying_price=None,buy_date = None,selling_date = None):
    max_profit = 0
    min_loss = float('inf')

    if(buying_price==None):
        for i in range(count):
            for j in range(i + 1, count):
                buying_price = stock_prices[i].get('closing_prize')
                selling_price = stock_prices[j].get('closing_prize')
                shares = 200

                profit = (selling_price - buying_price) * shares

                if profit > max_profit:
                    max_profit = profit
                    buy_date = stock_prices[i].get('date')
                    selling_date = stock_prices[j].get('date')
    else:
        buying_price = Decimal(buying_price) 
        index = 0
        for i, stock_price in enumerate(stock_prices):

            if stock_price['closing_prize'] == buying_price:
                index = i
                break
        # profit
        for j in range(index+1, count):
                selling_price = stock_prices[j].get('closing_prize')
                shares = 200
                profit = (selling_price - buying_price) * shares
                if profit >=0:
                    if profit > max_profit:
                        max_profit = profit
                        selling_date = stock_prices[j].get('date')       
                else:
                    if profit < min_loss:
                        min_loss = profit
                        selling_date = stock_prices[j].get('date')
                        
    buying_price = stock_prices.filter(date=buy_date).values()
    selling_price = stock_prices.filter(date=selling_date).values()
    # mean stock prize and standard deviation
    closing_prices = [stock_price.get('closing_prize') for stock_price in stock_prices]
    if len(stock_prices) >= 2:
        mean_stock_price = sum(closing_prices) / len(closing_prices) 
        standard_deviation = statistics.stdev(closing_prices)
    else:
        mean_stock_price = None
        standard_deviation = None
    return buy_date,selling_date,buying_price,selling_price, max_profit,mean_stock_price,standard_deviation

@api_view(['POST'])
def post_user(request):
    company = request.data.get('company_name')
    price = request.data.get('price')
    buy_date = parse_date(request.data.get('buy_date'))
    if(not UserProfile.objects.filter(company_name=company,stock_prize = price,buying_date=buy_date)):
        UserProfile.objects.create(company_name=company,stock_prize = price,buying_date=buy_date)
        return Response({"message":"success"})
    return Response({"message":"The user cannot buy more stocks on the same date."})

@api_view(['GET'])
def get_user_profile(request):
    company_name = request.data.get('company_name')
    price = request.data.get('price')
    buy_date = parse_date(request.data.get('buy_date')).date()
    end_date = datetime.now().date()
    if(not StockTrading.objects.filter(company__icontains=company_name, date=buy_date, closing_prize=price)):
            queryset=StockTrading.objects.filter(company__icontains=company_name, date=buy_date).values()
            id = queryset[0].get('id')-1
            price=StockTrading.objects.filter(id=id).values()[0].get('closing_prize')
            date=StockTrading.objects.filter(id=id).values()[0].get('date')
            stock_prices = StockTrading.objects.filter(company__icontains=company_name, date__range=(date, end_date)).values().order_by('date')
    else:
        stock_prices = StockTrading.objects.filter(company__icontains=company_name, date__range=(buy_date, end_date)).values().order_by('date')   
    count = stock_prices.count()
    data1 = StockTradingSerializer(stock_prices, many=True, context={'request': request}).data
    buy_date,selling_date,buying_price,selling_price, max_profit,mean_stock_price,standard_deviation = result(stock_prices,count,price,buy_date)
    
    return Response ({"message":data1,
                      "buy_date":buy_date,
                      "selling_date":selling_date,
                      "max_profit":max_profit,
                      "mean_stock_price":mean_stock_price,
                      "standard_deviation":standard_deviation,
                      "buying_price":buying_price,
                      "selling_price":selling_price})
   



