import types
import telebot
import warnings
import django
import os
import sys
from telebot import types, apihelper
from django.core.cache import cache
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from utils.verification.send_code import send_verification_code
from utils.verification.verification_type import get_verification_type
from utils.verification.check_code import check_verification_code

warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")

BOT_TOKEN = settings.BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')
apihelper.SESSION_TIME_TO_LIVE_IN_SECONDS = 60 * 60 * 24


@bot.message_handler(commands=['start'])
def welcome(message):
    print("start")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_button = types.KeyboardButton(
        text="Telefon raqamni yuboring.",
        request_contact=True
    )
    keyboard.add(keyboard_button)
    bot.send_message(message.from_user.id, "Telefon raqamni kiriting.", reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    print("second")
    cache.set("phone_number", message.contact.phone_number, timeout=60)
    verification_type_from_bot = get_verification_type(message.contact.phone_number)
    send_verification_code(phone_number=message.contact.phone_number,
                           verification_type=verification_type_from_bot)

    bot.send_message(message.from_user.id, text=F"{message.contact.phone_number}")


@bot.message_handler(commands=["code"], content_types=['text'])
def get_code(message):
    print("third")
    phone_number = cache.get("phone_number")
    print("phone_number:", phone_number)
    verification_type_ = get_verification_type(phone_number)
    code = message.text
    checked_code = check_verification_code(phone_number, verification_type_, code)
    print("checked_code : ", checked_code)


def my_commands():
    return [

        types.BotCommand('/start', 'Botni ishga tushurish'),
        types.BotCommand('/code', 'SMS dagi kodni kiritish'),
    ]




if __name__ == "__main__":
    print('started ...')
    bot.set_my_commands(commands=my_commands())
    bot.polling()
