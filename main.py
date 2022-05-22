import datetime
import telebot
import random
import os
from settings import token, quantity
from icrawler.builtin import GoogleImageCrawler

bot = telebot.TeleBot(token)

@bot.message_handler()
def commandBot(message):
    chat_id = message.from_user.id
    if message.text == '/start':
        bot.send_message(chat_id, 'Привет! Я могу найти изображение по твоему запросу, просто напиши что-нибудь в чат.')
    else:
        try:
            command = message.text
            os.mkdir(f'{chat_id}')
            bot.send_message(chat_id, 'Идёт поиск изображения')
            directory = f'{os.getcwd()}\{chat_id}'
            google_crawler = GoogleImageCrawler(storage={'root_dir':f'{directory}'})
            google_crawler.crawl(keyword=command, max_num=quantity)
            with open(os.path.join(directory, random.choice(os.listdir(directory))),'rb') as photo:
                photo = photo
                files = {'photo':photo}
                bot.send_photo(chat_id, photo, reply_to_message_id=message.id)
            print(files)
            today = datetime.datetime.today()
            newName = f'{chat_id}_{today.strftime(f"%Y-%m-%d-%H.%M.%S")}_{command}'
            os.rename(f'{chat_id}', newName)
            if not os.path.isdir('History'):
                os.mkdir('History')
            os.replace(newName, f'History/{newName}')
        except FileExistsError:
            bot.send_message(chat_id, 'Пожалуйста, дождитесь окончания прошлого поиска.')
            bot.register_next_step_handler_by_chat_id(chat_id, commandBot)
        
bot.polling(True)
