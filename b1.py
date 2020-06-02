import telebot;
bot = telebot.TeleBot('1101157557:AAEbuY7qdr9xHROQOEuAC5hZ3UyWWuz1S7U');
from telebot import types

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    
    if message.text == "Привет":

        bot.send_message(message.from_user.id, "Привет!")
        keyboard = types.InlineKeyboardMarkup()
    
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='answer')

        keyboard.add(key_yes)

        key_no = types.InlineKeyboardButton(text='Нет', callback_data='answer')

        keyboard.add(key_no)
        bot.send_message(message.from_user.id, text='Поиграем в Крестики-Нолики?', reply_markup=keyboard) 


    elif message.text == "/help":

        bot.send_message(message.from_user.id, "Напиши Привет")

    else:

        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
