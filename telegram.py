import telebot
import Database

bot = telebot.TeleBot("1628197070:AAFLvfUgbwO8qnY4YkQJ8yLHLoube-51GKc", parse_mode="MarkdownV2")
connection = Database.create_connection("test.db")
print("Telegram is working...")
@bot.message_handler(commands=['profit'])
def handle_command(message):
    msg = Database.profitCalc(connection)
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['altin'])
def handle_command(message):
    bot.send_message(message.chat.id,"Para altında kardeşim")

@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    bot.send_message(message.chat.id,'\U0001F4C8')


bot.polling()