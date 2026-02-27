# import telebot

# bot = telebot.TeleBot(token="8338108581:AAGoPJ1uP4moRPDGw7ADNV3nM6jSXAk_io4")

# savollarga_javob = {
#     "salom": "Salom! Qalaysiz?",
#     "isming nima": "Mening ismim Savol-Javob Bot",
#     "python nima": "Python — mashhur va oson dasturlash tili.",
#     "qayerdansan": "Men Python dasturlash tilida yozilganman.",
#     "xayr": "Xayr"
# }

# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(
#         message.chat.id,
#         "Salom qalesan!\ntuzumisan!"
#     )

# @bot.message_handler(func=lambda message: True)
# def answer(message):
#     user_text = message.text.lower()

#     for question in savollarga_javob:
#         if question in user_text:
#             bot.send_message(message.chat.id, savollarga_javob[question])
#             return

#     bot.send_message(
#         message.chat.id,
#         "Kechirasiz, bu savolga javob topa olmadim."
#     )

# print("Bot ishga tushdi...")
# bot.infinity_polling()


import telebot
from telebot.types import Message
from config import TOKEN


bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=["start"])
def start_handler(message: Message):
    bot.send_message(
        message.chat.id, f"ASSALOMU ALAYKUM !!! {message.from_user.full_name}!"
    )
    user = message.from_user
    first_name = user.first_name if user.first_name else ""
    last_name = user.last_name if user.last_name else ""
    username = f"@{user.username}" if user.username else ""
    user_id = user.id
    with open("userinfo.txt", "a") as file:
        file.write(f"{"⌄"*33}\n")
        file.write(f"Ismi:> {first_name}\n")
        file.write(f"Familyasi:> {last_name}\n")
        file.write(f"Foydalanuvchi nomi:> {username}\n")
        file.write(f"Telegram id:> {user_id}\n")
        file.write(f"{"⌄"*33}\n")


@bot.message_handler()
def echo(message: Message):
    bot.send_message(
        message.chat.id,
        f"Menda bunday buyruq yoq!!!\n"
        f"Biz yuborishingiz mumkin bolgan buyruqlar\n"
        f"{"⌄"*33}\n"
        f"Buyruq 1) /start ---> botni yangilash\n"
        f"{"^ "*35}\n",
    )


print("bot ishga tushdi")
bot.infinity_polling()
