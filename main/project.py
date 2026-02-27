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
