import os
import types
import environ
import telebot
import django
import warnings
from telebot import types
from pathlib import Path
from django.core.cache import cache

warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from utils.verification import send_code, verification_type, check_code

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

BOT_TOKEN = env('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')


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
    verification_type_from_bot = verification_type.get_verification_type(message.contact.phone_number)
    send_code.send_verification_code(phone_number=message.contact.phone_number,
                                     verification_type=verification_type_from_bot)

    bot.send_message(message.from_user.id, text=F"{message.contact.phone_number}")


@bot.message_handler(commands=["code"], content_types=['text'])
def get_code(message):
    print("third")
    phone_number = cache.get("phone_number")
    print("phone_number:", phone_number)
    verification_type_ = verification_type.get_verification_type(phone_number)
    code = message.text
    checked_code = check_code.check_verification_code(phone_number, verification_type_, code)
    print("checked_code : ", checked_code)


def my_commands():
    return [

        types.BotCommand('/start', 'Botni ishga tushurish'),
        types.BotCommand('/code', 'SMS dagi kodni kiritish'),
    ]


if __name__ == "__main__":
    print('started ...')
    bot.set_my_commands(commands=my_commands())
    bot.infinity_polling()
