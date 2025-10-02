import os
import types
import messages
import environ
import telebot
import django
from telebot import types
from pathlib import Path
import warnings

warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from utils.verification import send_code, verification_type

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

BOT_TOKEN = env('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')


@bot.message_handler(commands=['start'])
def welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_button = types.KeyboardButton(
        text="Telefon raqamni yuboring.",
        request_contact=True
    )
    keyboard.add(keyboard_button)
    bot.send_message(message.from_user.id, "Telefon raqamni kiriting.", reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    verification_type_from_bot = verification_type.get_verification_type(message.contact.phone_number)
    print(verification_type_from_bot)
    send_code.send_verification_code(phone_number=message.contact.phone_number,
                                     verification_type=verification_type_from_bot)

    bot.send_message(message.from_user.id, text=F"{message.contact.phone_number}")


@bot.message_handler(commands=['search'])
def search_handler(message):
    print('search is working')
    msg = bot.send_message(chat_id=message.from_user.id, text=messages.SEARCH)
    # bot.register_next_step_handler(msg, sear_wiki)


"""def sear_wiki(message):
    print('serach wiki is working')
    result_text = wiki_config.WikiSearch(message.text).get_result()
    if result_text is not None:
        bot.send_message(message.from_user.id, text=f"{result_text}")
    else:
        bot.send_message(message.from_user.id, text=messages.NOT_FOUND)
"""


def my_commands():
    return [

        types.BotCommand('/start', 'Botni ishga tushurish'),
        types.BotCommand('/contact', "Ro'yxatdan o'tish"),
        types.BotCommand('/search', 'Malumotlarni qidirsh')
    ]


if __name__ == "__main__":
    print('started ...')
    bot.set_my_commands(commands=my_commands())
    bot.infinity_polling()
