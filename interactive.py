from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from cvs import *
from hourly_checknalert import getPriceMsg
app = Flask(__name__)
from translation_and_language_sentiment import *
import requests

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    message_received, lang = translate_text("en", request.form['Body'])
    phone_num_from = request.form["From"]
    mra = message_received.split(' ');

    if mra[0] == "activate":
        url = 'http://localhost:3000/activate'
        post_data = {'phone_num': phone_num_from, 'code': str(mra[1])}
        requests.post(url, data = post_data)
        return ""

    url = "http://localhost:3000/get_user"
    post_data = {'phone_num': phone_num_from}
    user = requests.post(url, data = post_data).json()["user"]
    print(user)
    if ("_fieldsProto" not in user) or ("activated" not in user["_fieldsProto"]) or (user["_fieldsProto"]["activated"] != "y"): 
        print("User doesn't exist or not activated!")
        return ""

    #print(message_received)
    message_to_send = ""

    currency_name = mra[0];

    news_response = getNews(currency_name, num=1)
    news0 = news_response["articles"][0];
    news0_message_to_convey = "1. " + news0["title"] + ".\n" + \
    "per " + news0["source"]["name"] + ": " + news0["url"] + "\n"

    reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                         client_secret=os.getenv("REDDIT_CLIENT_SECRET"), password=os.getenv("REDDIT_PASSWORD"),
                         user_agent='PRAW', username=os.getenv("REDDIT_USER_NAME"))

    #print(reddit.user.me())
    reddit_message_to_convey = f"Hot discussion on {currency_name} since last hour:\n"

    for post in reddit.subreddit(currency_name).top("day", limit=1):
        reddit_message_to_convey += f"{post.title} {post.url} {post.ups} upvotes, {post.num_comments} comments.\n"

    ai_advice_message_to_convey = "AI Advice: " + getAIAdvice(currency_name)["conclusion"] \
    + ".\n"

    if (len(mra) == 1):
        lang = "en"
        message_to_send += f"{currency_name}'s current price is {getCurrentPrice(currency_name)[0:7]} USD.\n\n"
        message_to_send += f"News headlines on {currency_name}:\n{news0_message_to_convey}\n"
        message_to_send += reddit_message_to_convey + "\n"
        message_to_send += ai_advice_message_to_convey
        message_to_send += "\n"
    else:
        for attr in mra:
            if (attr == "price"):
                message_to_send += getPriceMsg(currency_name)
                message_to_send += "\n"
            elif (attr == "news"):
                message_to_send += f"News headlines on {currency_name}:\n{news0_message_to_convey}"
                message_to_send += "\n"
            elif (attr == "discussion"):
                message_to_send += reddit_message_to_convey
                message_to_send += "\n"
            elif (attr == "advice"):
                message_to_send += ai_advice_message_to_convey
                message_to_send += "\n"
            else:
                pass

    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message(translate_text(lang, message_to_send)[0])

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
