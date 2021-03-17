import telebot

bot = telebot.TeleBot("1628197070:AAFLvfUgbwO8qnY4YkQJ8yLHLoube-51GKc", parse_mode="MarkdownV2")

@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    print(message.chat.id)

#-1001408874432 GRUP
#1487856885 EMRE

msg = input()
while len(msg)!=0:
    bot.send_message(-1001408874432, msg)
    msg = input()


bot.polling()
