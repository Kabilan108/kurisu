"""

"""

# Imports
from flask import Flask, request
from kurisu.credentials import BOT_TOKEN, BOT_USERNAME, HEROKU_URL
import telegram
import re

# Global variables
global bot
global TOKEN
global URL

# Initialize bot
TOKEN = BOT_TOKEN
URL = HEROKU_URL
bot = telegram.Bot(token=TOKEN)

# Initialize Flask app
app = Flask(__name__)


@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    """
    App route function for `/{token}` endpoint.
    
    This function is called when Telegram sends a POST request to your bot's
    endpoint. It will parse the request and call the appropriate function
    to handle the request.
    """

    # Retrieve message as JSON
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # Retrieve chat identifiers
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Decode message text
    text = update.message.text.encode('utf-8').decode()

    #debug
    print("Got text message :", f"chat_id: {chat_id}", f"msg_id: {msg_id}", 
          f"text: {text}", sep="\n")
    
    # Welcome message
    if text == "/start":
        bot.send_message(
            chat_id=chat_id, 
            reply_to_message_id=msg_id,
            text="""
Hello, I am Makise Kurisu, your GPT4-powered assint.
            """
        )

    else:
        try:
            # Send a photo based on numeric characters in the message
            text = re.sub(r"\W", "_", text)
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            bot.send_photo(chat_id=chat_id, reply_to_message_id=msg_id, photo=url)
        except Exception:
            bot.send_message(
                chat_id=chat_id,
                reply_to_message_id=msg_id,
                text="There was a problem in the name you used. Please try again."
            )

    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    """
    App route function for `/setwebhook` endpoint.

    This function is called when you want to set a webhook for your bot. It
    will set the webhook to the URL of your Heroku app.
    """

    s = bot.set_webhook(f'{URL}{TOKEN}')

    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
    

@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)
