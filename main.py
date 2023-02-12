import openai
import telebot
import boten

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

global sizeOfPhoto 

openai.api_key = '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'
openai.Model.list()
bot = telebot.TeleBot(boten.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('stickerGoodMorning.webp','rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Створення нового зображення")
    markup.add(item1)

    bot.send_message(message.chat.id, "Vіtаєmо, {0.first_name}!\n Ja - <b>{1.first_name}</b>, bot, jakyj bulo stvoreno dḷa testuvaṇṇa Calendar API.".format(message.from_user, bot.get_me()),
    parse_mode='html', reply_markup=markup) 

@bot.message_handler(commands=['exit'])
def exit(message):
    #sti = open('stickerGoodBye.webp','rb')
    #bot.send_sticker(message.chat.id, sti)
    sti = open('stickerZaluzhnyi.webp','rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Nechaj s̈astyṭ, dryże!".format(message.from_user, bot.get_me()))
    bot.stop_polling()

def markup_inline():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("256x256", callback_data = "256x256"),
        InlineKeyboardButton("512x512", callback_data = "512x512"),
        InlineKeyboardButton("1024x1024", callback_data = "1024x1024")
    )
    return markup

@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    global sizeOfPhoto
    if call.data == "256x256":
        sizeOfPhoto = "256x256"
    elif call.data == "512x512":
        sizeOfPhoto = "512x512"
    elif call.data == "1024x1024":
        sizeOfPhoto = "1024x1024"

    bot.send_message(call.message.chat.id, "Ви обрали розмір " + sizeOfPhoto + "")
    send = bot.send_message(call.message.chat.id, "Введіть опис для згенерованого фото англійською")
    bot.register_next_step_handler(send, event_create, sizeOfPhoto)

@bot.message_handler(content_types=['text'])
def generateImage(message):
   if message.chat.type == 'private':
        if message.text == 'Створення нового зображення':           
            bot.send_message(message.chat.id, "Оберіть розмір бажаного згенерованого фото".format(message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup_inline())            
        else:
            bot.send_message(message.chat.id, 'I don`t understand you...')

def event_create(message, sizeOfPhoto):
    try:
        photo = openai.Image.create(
        prompt = message.text,
        n = 1,
        size = sizeOfPhoto
        )
        image_url = photo['data'][0]['url']
        bot.send_message(message.chat.id, 'Зображення на запит *' + message.text + '* було згенеровано', parse_mode= "Markdown")
        bot.send_photo(message.chat.id, image_url)
    except openai.error.OpenAIError as e:
        sti = open('stickerRusnia.webp','rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, "Помилка у безпечності введеного запиту. Спробуйте ще раз.")

bot.polling(none_stop=True)

'''"Russian soldier stole a toilet from Ukraine"'''