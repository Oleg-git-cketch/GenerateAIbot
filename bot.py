import telebot
import database as db
import img_gen as ig
from deep_translator import GoogleTranslator



bot = telebot.TeleBot('7952352811:AAEqgtz9v94gFEWoFnLHiTEZYGI2Q7AJylQ')


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    if db.check_count(user_id):
        bot.send_message(user_id, 'Напишите запрос и я сгенерирую по нему фото!')
        bot.register_next_step_handler(message, get_prompt)
    else:
        db.register(user_id)
        bot.send_message(user_id, 'Напишите запрос и я сгенерирую по нему фото!')
        bot.register_next_step_handler(message, get_prompt)

def get_prompt(message):
    user_id = message.from_user.id
    prompt = message.text

    if db.check_count(user_id) <= 5:
        try:
            prompt = GoogleTranslator(source='auto', target='en').translate(message.text)
            image = ig.get_link(prompt)
            bot.send_photo(user_id, photo=image)
            bot.send_message(user_id, 'Готово!')
            db.add_count(user_id)
            bot.register_next_step_handler(message, get_prompt)
        except:
            bot.send_message(user_id, 'Видимо, ошибка в запросе. Попробуйте еще раз')
            bot.register_next_step_handler(message, get_prompt)
    else:
        bot.send_message(user_id, 'Похоже, что ты истратил все токены.\n'
                                  'Оплати подписку или жди следующего месяца')

bot.polling(non_stop=True)