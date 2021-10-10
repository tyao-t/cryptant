import os
from dotenv import load_dotenv
import smtplib
import praw
from twilio.rest import Client
from cvs import *
from pymongo import MongoClient
import unidecode as ud
import time

load_dotenv()

def getPriceMsg(name="Bitcoin"):
    this_hour_price = getCurrentPrice(name)
    last_hour_price = getPriceAnHourAgo(name)
    price_eight_hrs_ago = getPriceEightHrsAgo(name)

    percent_change1 = (float(this_hour_price) / float(last_hour_price) - 1.000000) * 100;
    percent_change2 = (float(this_hour_price) / float(price_eight_hrs_ago) - 1.000000) * 100

    sign1 = None
    if percent_change1 > 0:
        sign1 = "🔺 " + str(percent_change1)[0:5] + "%"
    else:
        sign1 = "🔻 " + str(percent_change1)[1:6] + "%"

    sign2 = None
    if percent_change2 > 0:
        sign2 = "🔺 " + str(percent_change2)[0:5] + "%"
    else:
        sign2 = "🔻 " + str(percent_change2)[1:6] + "%"

    price_message_to_convey = f"There's some observable change in {name}'s current price! It is {this_hour_price[0:7]}, \
    \n{sign1} from last hour, \nand {sign2} from 8 hours ago.\n"
    return price_message_to_convey

def provideHourlyAlert(currency_name = "Bitcoin", phone_num = os.getenv("MY_PHONE_NUM"), email_to = os.getenv("DEFAULT_EMAIL_TO"), name_to="there"):
    reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                         client_secret=os.getenv("REDDIT_CLIENT_SECRET"), password=os.getenv("REDDIT_PASSWORD"),
                         user_agent='PRAW', username=os.getenv("REDDIT_USER_NAME"))
    #print(reddit.user.me())

    reddit_message_to_convey = f"Hot discussion on {currency_name} since last hour:\n"

    for post in reddit.subreddit(currency_name).top("hour", limit=2):
        reddit_message_to_convey += f"{post.title} {post.url} {post.ups} upvotes, {post.num_comments} comments.\n"

    price_message_to_convey = getPriceMsg(currency_name)
#print(price_message_to_convey)

    news_response = getNews(currency_name, num=1, frame="1D")
    news0 = news_response["articles"][0];
    news0_message_to_convey = news0["title"] + ".\n" + \
    "per " + news0["source"]["name"] + ": " + news0["url"] + "\n"

    ai_advice_message_to_convey = "AI Advice: " + getAIAdvice(currency_name)["conclusion"] \
    + ".\n"

    greeting_message = f"Hi {name_to}!\n"
    full_message_to_convey = greeting_message + "\n" + price_message_to_convey + "\n" + "News headline:\n" + news0_message_to_convey + \
    "\n" + reddit_message_to_convey + "\n" + ai_advice_message_to_convey;
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
            msg=f"Subject:{currency_name} Alert\n\n{full_email_to_convey}"
        )"""

#client = MongoClient('mongodb+sr4.mongodb.net/hdb?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
#db = client.get_database('hdb')
#people = db.people
if __name__ == "__main__":
    provideHourlyAlert(name_to = "Tianhao")
