import os
from dotenv import load_dotenv
from twilio.rest import Client
from cvs import *
import unidecode as ud
import time

load_dotenv()

CUR_DATE = dt.datetime.now().strftime('%Y-%m-%d')

def provideDailyUpdate(currency_name = "Bitcoin", phone_num = os.getenv("MY_PHONE_NUM"), email_to = "", name_to="there"):
    percent_change = (float(getCurrentPrice(currency_name)) / float(getYesterdayPrice(currency_name)) - 1.000000) * 100;

    sign = None
    if percent_change > 0:
        sign = "🔺 " + str(percent_change)[0:5] + "%"
    else:
        sign = "🔻 " + str(percent_change)[1:6] + "%"

    high_price = getTodayHighPrice(currency_name)[0:7]
    low_price = getTodayLowPrice(currency_name)[0:7]

    price_message_to_convey = CUR_DATE + " :Today's closing price of " + currency_name + " is " + getCurrentPrice(currency_name)[0:7] + " USD" + \
    ", " + sign + " from yesterday's closing price." + " High: " + high_price + " USD, Low: " + low_price + " USD.\n"
    #print(price_message_to_convey)

    news_response = getNews(currency_name, num=2)
    news0 = news_response["articles"][0];
    news0_message_to_convey = "1. " + news0["title"] + ".\n" + \
    "per " + news0["source"]["name"] + ": " + news0["url"] + "\n"

    news1 = news_response["articles"][1];
    news1_message_to_convey = "2. " + news1["title"] + "\n" + \
    "per " + news1["source"]["name"] + ": " + news1["url"] + "\n"

    ai_advice = getAIAdvice(currency_name)
    ai_advice_message_to_convey = "AI Advice: " + ai_advice["conclusion"] \
    + ".\n"
    greeting_message = f"Hi {name_to}!\n"
    full_message_to_convey = greeting_message + "\n" + price_message_to_convey + "\n" + "News headlines:\n" + news0_message_to_convey + news1_message_to_convey + \
    "\n" + ai_advice_message_to_convey;
    print(full_message_to_convey)

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(messaging_service_sid=os.getenv("TWILIO_MESSAGING_SERVICE_SID"), body=full_message_to_convey, \
    to=phone_num)

    """
    my_email = os.getenv("MY_EMAIL")
    my_password = os.getenv("MY_EMAIL_PASSWORD")
    full_email_to_convey = full_message_to_convey.replace("🔺", "up")
    full_email_to_convey = full_email_to_convey.replace("🔻", "down")
    full_email_to_convey = ud.unidecode(full_email_to_convey)
    with smtplib.SMTP("outlook.office365.com") as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email_to,
            msg=f"Subject:{currency_name} Daily Feed\n\n{full_email_to_convey}"
        )"""

"""client = MongoClient('mongodb+srv://tyao_admin:rriveryth7@cluster-telus-ehs.4nek4.mongodb.net/hdb?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
db = client.get_database('hdb')
people = db.people"""
#print(list(people.find()))
provideDailyUpdate()
"""
if __name__ == "__main__":
    for person in list(people.find()):
        #print(person["name"] + " " + person["email"] + "\n")
        provideDailyUpdate(name_to = person["name"], email_to = person["email"])
        time.sleep(40) """
