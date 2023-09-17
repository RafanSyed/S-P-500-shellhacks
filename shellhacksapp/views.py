from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse 
import yfinance as yf
from .models import Product
from .models import *
from .dict import companies_500
from django.shortcuts import render, reverse
from .models import Company 


def hello(request):
    return render(request, 'main.html')





def get_financial_data(request):
    companies_data = {
        "GOOGL": "Google",
        "AAPL": "Apple",
        "MSFT": "Microsoft"
    }

    data_fields = ["regularMarketPrice", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "profitMargins", "averageVolume", "regularMarketVolume", "trailingPE"]

    company_data = {}

    for symbol, name in companies_data.items():
        try:
            stock = yf.Ticker(symbol)
            data = stock.info
            company_data[name] = {field: data.get(field) for field in data_fields}
        except Exception as e:
            print(f"Error fetching data for {name} ({symbol}): {str(e)}")

    for name, data in company_data.items():
        print(f"Data for {name}:")
        
       

        print(f"52-Week High:           ${data['fiftyTwoWeekHigh']:.2f}")
        print(f"52-Week Low:            ${data['fiftyTwoWeekLow']:.2f}")
        print(f"Profit Margin:           {data['profitMargins']:.2%}")
        print(f"Average Volume:          {data['averageVolume']:,} shares")
        print(f"Volume:                  {data['regularMarketVolume']:,} shares")
        print(f"Price-to-Earnings Ratio: {data['trailingPE']:.2f}")
        print("\n")
    context = {'company_data': company_data}

   
    return render(request, 'company_data_template.html', context)




def google_data(request):
   
    ticker_symbol = "GOOG"

    # Fetch Google's stock data
    goog = yf.Ticker(ticker_symbol)

    # Get the user's input from the query parameter 'search_query'
    user_input = request.GET.get('search_query')

  
    stock_info = {
        "company_name": goog.info["longName"],  
        "total_price": goog.history(period="1d")["Close"].iloc[0],
        "week_high": goog.history(period="1y")["High"].max(),
        "week_low": goog.history(period="1y")["Low"].min(),
        "profit_margin": goog.info["profitMargins"] * 100,
        "average_volume": goog.history(period="1y")["Volume"].mean(),
        "pe_ratio": goog.info["trailingPE"]
    }

   
    context = {
        "stock_info": stock_info,
        "user_input": user_input, 
    }


    return render(request, 'google_data_template.html', context)

def comparison(request):
    return render(request, 'comparison.html')



from django.shortcuts import render, redirect
from .models import Company  

def get_company_data(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name_firstone')

      
        company = Company.objects.filter(name__iexact=company_name).first()

        if company:
          
            request.session['company_name_firstone'] = company_name
        else:
            print("Company not found")
   

      
        company_tickers = companies_500

        # Check if the selected company name exists in the dictionary
        if company_name in company_tickers:
            ticker_symbol = company_tickers[company_name]
        else:
            print("Company not in S&P 500 ")
            return render(request, 'error_template.html', {"error_message": "Company not in S&P 500"})

        try:
            # Fetch the stock data for the selected company
            company_stock = yf.Ticker(ticker_symbol)

            # Get the relevant stock information
            stock_info = {
                'company_name': company_name,
                "total_price": company_stock.history(period="1d")["Close"].iloc[0],
                "week_high": company_stock.history(period="1y")["High"].max(),
                "week_low": company_stock.history(period="1y")["Low"].min(),
                "profit_margin": company_stock.info["profitMargins"] * 100,
                "average_volume": company_stock.history(period="1y")["Volume"].mean(),
                "pe_ratio": company_stock.info["trailingPE"]
            }

            # Create a context dictionary to pass the data to the template
            context = {"stock_info": stock_info, "selected_company": company_name}

            # Render the template with the data
            return render(request, 'google_data_template.html', context)
        except Exception as e:
            error_message = f"Error fetching data for {company_name}: {str(e)}"
            print(error_message)

  
    return render(request, 'main.html')




def comparison_step_one(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company = Company.objects.filter(name__iexact=company_name).first()

        if company:
         
            request.session['company_name_1'] = company_name
            return redirect('comparison_step_two')
        else:
            print("Company not found")
       
        
     
        return redirect(reverse('shellhacksapp:comparison_two'))

    return render(request, 'comparison.html')

def comparison_step_two(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        
        request.session['company_name_2'] = company_name
        return redirect('shellhacksapp:comparison_result')

    return render(request, 'comparison_two.html')


def comparison_result(request):
    company_name_1 = request.session.get('company_name_1')
    company_name_2 = request.session.get('company_name_2')

    # Check if both company names are available in the session
    if company_name_1 and company_name_2:
        
        company_tickers = companies_500
        ticker_symbol_1 = company_tickers.get(company_name_1)
        ticker_symbol_2 = company_tickers.get(company_name_2)

        if ticker_symbol_1 and ticker_symbol_2:
            try:
              
                company_stock_1 = yf.Ticker(ticker_symbol_1)
                company_stock_2 = yf.Ticker(ticker_symbol_2)

               
                stock_info_1 = {
                    'company_name': company_name_1,
                    "total_price": company_stock_1.history(period="1d")["Close"].iloc[0],
                    "week_high": company_stock_1.history(period="1y")["High"].max(),
                    "week_low": company_stock_1.history(period="1y")["Low"].min(),
                    "profit_margin": company_stock_1.info["profitMargins"] * 100,
                    "average_volume": company_stock_1.history(period="1y")["Volume"].mean(),
                    "pe_ratio": company_stock_1.info["trailingPE"]
                }

                stock_info_2 = {
                    'company_name': company_name_2,
                    "total_price": company_stock_2.history(period="1d")["Close"].iloc[0],
                    "week_high": company_stock_2.history(period="1y")["High"].max(),
                    "week_low": company_stock_2.history(period="1y")["Low"].min(),
                    "profit_margin": company_stock_2.info["profitMargins"] * 100,
                    "average_volume": company_stock_2.history(period="1y")["Volume"].mean(),
                    "pe_ratio": company_stock_2.info["trailingPE"]
                }

                
                context = {
                    "stock_info_1": stock_info_1,
                    "stock_info_2": stock_info_2,
                }

               
                return render(request, 'comparison_result.html', context)
            except Exception as e:
                error_message = f"Error fetching data: {str(e)}"
                print(error_message)

   
    return render(request, 'comparison_result.html')
