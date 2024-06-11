

#Importando bibliotecas do projeto
import os
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from datetime import timedelta

#Construindo conexão com API
from dotenv import load_dotenv


#Get the API_Key
load_dotenv()

API_key = os.getenv('API_KEY')


#Armazenando retornos das consultas em uma lista
stocks = ['AAPL','MSFT','AMZN','NVDA','GOOGL','TSLA','GOOG','BRK.B','META','UNH','XOM','LLY','JPM','JNJ','V','PG','MA','AVGO','HD','CVX']

stocks_info = []


for stock in stocks:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_key}'
    response = requests.get(url)
    stocks_info.append(response.json())


#Construindo dataframe com as 100 observações de uma respectiva ação
register_list = []


for i in range(len(stocks_info)):
    for day in stocks_info[i]['Time Series (Daily)'].keys():
        new_register = {'Stock_Code':stocks_info[i]['Meta Data']['2. Symbol'],
                        'Day':day,
                        'Opening_Value':stocks_info[i]['Time Series (Daily)'][day]['1. open'], 
                        'Highest_Value':stocks_info[i]['Time Series (Daily)'][day]['2. high'],
                        'Lowest_Value':stocks_info[i]['Time Series (Daily)'][day]['3. low'],
                        'Closing_Value':stocks_info[i]['Time Series (Daily)'][day]['4. close'],
                        'Volume':stocks_info[i]['Time Series (Daily)'][day]['5. volume']
                        }
        
        register_list.append(new_register)
        #dicionary.update(new_register1)

raw_data = pd.DataFrame(register_list)


#Creating a backup dataframe before the cleaning and manipulation process
cleaning_data = raw_data.copy()


#Casting the variables to proper format
cleaning_data['Opening_Value'] = list(map(lambda x: float(x), cleaning_data['Opening_Value']))
cleaning_data['Highest_Value'] = list(map(lambda x: float(x), cleaning_data['Highest_Value']))
cleaning_data['Lowest_Value'] = list(map(lambda x: float(x), cleaning_data['Lowest_Value']))
cleaning_data['Closing_Value'] = list(map(lambda x: float(x), cleaning_data['Closing_Value']))
cleaning_data['Volume'] = list(map(lambda x: int(x), cleaning_data['Volume']))
cleaning_data['Day'] = list(map(lambda x: datetime.strptime(x, '%Y-%m-%d'), cleaning_data['Day']))
cleaning_data['WeekDay'] = list(map(lambda x: datetime.strftime(x, '%A'), cleaning_data['Day']))
cleaning_data['Month_Name'] = list(map(lambda x: datetime.strftime(x, '%B'), cleaning_data['Day']))


#Adding more columns of new time intervals
cleaning_data['Year'] = list(map(lambda x: x.year, cleaning_data['Day']))
cleaning_data['Month'] = list(map(lambda x: x.month, cleaning_data['Day']))
cleaning_data['Week'] = list(map(lambda x: x.week, cleaning_data['Day']))
cleaning_data['Quarter'] = list(map(lambda x: x.quarter, cleaning_data['Day']))


#Importing companies names x stocks
companies_stocks_names = pd.read_csv('Stock_Companies_Names.csv', sep=';', names=['Company_Name','Stock_Code'])
companies_stocks_names


#Organizing the columns on the final dataframe
cleaned_data = cleaning_data.merge(companies_stocks_names, on='Stock_Code')
cleaned_data = cleaned_data[['Company_Name','Stock_Code','Year','Month','Month_Name','Week', 'Day', 'WeekDay', 'Quarter','Opening_Value', 'Highest_Value', 'Lowest_Value',
       'Closing_Value', 'Volume']]


#Creating a new column for the daily variation (The daily variation is calculated using the current day closing value and the day before closing value)
Daily_Closing_Variation = []


#Creating a new column for the daily variation (The daily variation is calculated using the current day closing value and the day before closing value)
try:
    
    for i,stock_code in enumerate(cleaned_data['Stock_Code']):
        if (cleaned_data['Stock_Code'][i] == cleaned_data['Stock_Code'][i+1]):
            daily_variation = ((cleaned_data[(cleaned_data['Stock_Code'] == stock_code) & (cleaned_data['Day'] == cleaned_data['Day'][i])]['Closing_Value'])[i] - (cleaned_data[(cleaned_data['Stock_Code'] == stock_code) & (cleaned_data['Day'] == cleaned_data['Day'][i+1])]['Closing_Value'])[i+1])/(cleaned_data[(cleaned_data['Stock_Code'] == stock_code) & (cleaned_data['Day'] == cleaned_data['Day'][i+1])]['Closing_Value'])[i+1]*100

            Daily_Closing_Variation.append(daily_variation)

        elif (cleaned_data['Stock_Code'][i] != cleaned_data['Stock_Code'][i+1]):
            daily_variation = '-'

            Daily_Closing_Variation.append(daily_variation)

except:
    Daily_Closing_Variation.append('0')


cleaned_data['Daily_Closing_Variation'] = [float(i) for i in Daily_Closing_Variation]
