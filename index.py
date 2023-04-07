from flask import Flask, request, abort
from chatGPT import ChatGPT
from IPython.display import Markdown, display
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
# 為了處理json字串引入的模組
import json

app = Flask(__name__)
chatgpt = ChatGPT()
line_bot_api = LineBotApi('dw7F38Eky44laTlVAnBEW9JX9PH8vP4t2k3rQlLX1s4RYLmfce/L2K+g+cx3xEl0CztGTYeG9LLjhTwuxX3CZGKZx7OEhbW88OLhgGjv28E/L9WFgux7OCUQsmV45mHaNIQnLunqJAEs/wY3ix4n3wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ed4533c06497af6784dda91261f6b100')
isAnswer = 0

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global isAnswer 
    #  想了解問題1: event的內容到底是甚麼
    print(event)
    if event.message.type != "text":
        return
    if event.message.text == "請出題":
        chatgpt.add_msg(f"Human:以上有5題數學問題，我希望你讀懂這4題數學問題然後把你自己當作一個數學出題老師，思考要如何跟據這5題的概念出一個嶄新的題目，題目為4選1選擇題，請附上詳解與解答(請完整說明你是根據第幾題出出來的）")
        reply_msg = chatgpt.get_response()
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg)
        )
if __name__ == "__main__":
    app.run( host = "minniemachine.club",ssl_context=('/etc/letsencrypt/live/minniemachine.club/fullchain.pem', '/etc/letsencrypt/live/minniemachine.club/privkey.pem'))