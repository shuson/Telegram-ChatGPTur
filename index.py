import os,telegram
from flask import Flask, request


URL = os.getenv("URL")

BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

bot = telegram.Bot(token=BOT_TOKEN)
hook_url = "{URL}bot{HOOK}/".format(URL=URL, HOOK=BOT_TOKEN)

bot.setWebhook(hook_url)

app = Flask(__name__)


@app.route("/bothook", methods=["POST"])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode("utf-8").decode()

    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = "Hi! I respond by echoing messages. Give it a try!"
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    else:
        bot.sendMessage(chat_id=chat_id, text=text)

    return "ok"


@app.route("/getme", methods=["GET"])
def set_webhook():
    return hook_url


@app.route("/")
def index():
    return "Hello, welcome to the telegram bot index page"


if __name__ == "__main__":
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)