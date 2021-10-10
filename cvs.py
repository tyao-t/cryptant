import os
from dotenv import load_dotenv
import requests
import datetime as dt
import smtplib
import praw

load_dotenv()

CUR_DATE = dt.datetime.now().strftime('%Y-%m-%d')
CUR_TIME = dt.datetime.now(tz=dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
TIME_AN_HR_AGO = (dt.datetime.now(tz=dt.timezone.utc) - dt.timedelta(hours = 1)).strftime('%Y-%m-%dT%H:%M:%S')

PRICE_ENDPOINT = 'https://cryptantapi.root.sx/getCandles/'

def getCurrentPrice(name):
    price_response = requests.get(PRICE_ENDPOINT + f"{name}/1h").json()
    return price_response[-1]["close"]

def getYesterdayPrice(name):
    price_response = requests.get(PRICE_ENDPOINT + f"{name}/1D").json()
    return price_response[-2]["close"]

def getTodayHighPrice(name):
    price_response = requests.get(PRICE_ENDPOINT + f"{name}/1D").json()
    return price_response[-1]["high"]

def getTodayLowPrice(name):
    price_response = requests.get(PRICE_ENDPOINT + f"{name}/1D").json()
    return price_response[-1]["low"]

def getPriceAnHourAgo(name):
    price_response = requests.get(PRICE_ENDPOINT + f"{name}/1h").json()
    return price_response[-2]["close"]

def getPriceEightHrsAgo(name):
    price_response = requests.get(PRICE_ENDPOINT + f"{name}/1h").json()
    return price_response[-9]["close"]

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_params = {
    "apiKey": NEWS_API_KEY,
    "q": "",
    "from": CUR_DATE,
    "to": CUR_DATE,
    "sortBy": "popularity",
    "pageSize": "",
    "page": "1"
}

def getNews(name, num="1", frame="1D"):
    news_params["qInTitle"] = name
    news_params["pageSize"] = num
    if (frame == "1h"):
        news_params["from"] = TIME_AN_HR_AGO
        news_params["to"] = CUR_TIME
    news_response = requests.get(NEWS_ENDPOINT, params = news_params).json()
    return news_response

def getAIAdvice(name):
    return requests.get("https://cryptantapi.root.sx/getPrediction/" + name).json()
