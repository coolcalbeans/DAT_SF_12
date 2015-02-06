# -*- coding: utf-8 -*-
"""
Spyder Editor
Author: Vijay Duraipalam
"""
from __future__ import division
import datetime as dt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import re

#Declare Global Constants
CONST_TABLE_START = 'Index'
CONST_TABLE_END = 'Change'
CONST_FINVIZ_URL = 'http://finviz.com/quote.ashx?t='
CONST_TICKER_LIST = 'http://www.sharadar.com/meta/tickers.txt'

#Function to find the Table Start and Table End Index on the FinViz Page
def getStartEndAttributeTDIndex(tags):
    for i in range(len(tags)):
        if tags[i].string == None or tags[i].string == '\n':    
            continue
        elif tags[i].string.upper() == CONST_TABLE_START.upper():
            i_startCount = i
        elif tags[i].string.upper() == CONST_TABLE_END.upper():
            i_endCount = i+1
            break
    return i_startCount, i_endCount

#Function to see if ticker is not foung when scraping FinViz. Given Error String is checked.
def checkTickerNotFound(soup, s_ticker):
    s_errString = 'We cover only stocks and ETFs listed on NYSE, NASDAQ, and AMEX'
    #print("Error String=\n" + s_errString)
    #print soup.find_all(text = re.compile(s_errString))
    if len(soup.find_all(text = re.compile(s_errString))) > 0:
        return True
    return False
    

startTime = dt.datetime.now()
print(startTime.strftime('%H:%M:%S %m/%d/%Y') + " :: Starting FinViz Parser")

url_quandl = CONST_TICKER_LIST

df_QuandlData = pd.read_table(url_quandl)
df_QuandlData = df_QuandlData[df_QuandlData['Currency'] == 'USD']
#Dropping following columns out of the the Quandl Dataframe
df_QuandlData.drop('CUSIP', axis=1, inplace=True)
df_QuandlData.drop('ISIN', axis=1, inplace=True)
df_QuandlData.drop('Currency', axis=1, inplace=True)
df_QuandlData.drop('Wiki Ticker', axis=1, inplace=True)
print df_QuandlData.head()
print df_QuandlData.tail()
print ("Length of Quandl Data frame: %d" %len(df_QuandlData))

ls_ticker = df_QuandlData['Ticker'].tolist()
print ls_ticker
d_ticks = {}

#ls_ticker = ['ABMC', 'XON', 'XOM', 'AAPL']
#For each ticker scrape the FinViz website for ticker properties
for s_ticker in ls_ticker:
    url = CONST_FINVIZ_URL + s_ticker
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    print(soup.title.string + " : " + s_ticker)
    
    if(s_ticker not in soup.title.string):
        print("Ticker: "+s_ticker+" not found in FinViz")
    else:
        assert(s_ticker in soup.title.string)
    
    #Find all column attributes on the FinViz Stock Ticker Webpage
    if checkTickerNotFound(soup, s_ticker):
        print('\t---- Ticker '+s_ticker+' not found in FinViz')
        continue
    else:        
        tags = soup.find_all('td')    
        i_startCount, i_endCount = getStartEndAttributeTDIndex(tags)
        
        d_tickProperties = {}
        for i in range(i_startCount, i_endCount+1, 2):
            #print tags[i].string, tags[i+1].string
            d_tickProperties[tags[i].string] = tags[i+1].string    
    
        #Populating the ticker properties into the ticker dictionary
        d_ticks[s_ticker] = d_tickProperties
        #Request URL Request Cleanup
        r.cookies.clear()
        time.sleep(0.009) 
    
df_ticker = pd.DataFrame(d_ticks)
df_ticker = df_ticker.transpose()
print("\nPopulated Ticker Attributes are:")
print df_ticker.head()
print ("Length of Populated Ticker Attributes Data frame: %d" %len(df_ticker))
df_ticker.to_excel('Ticker Attributes Output.xlsx')

endTime = dt.datetime.now()
runTime = endTime - startTime 
print(endTime.strftime('\n%H:%M:%S %m/%d/%Y') + " :: Ending FinViz Parser")
print("FinViz Parser Total Run Time " + str(runTime)[:7])