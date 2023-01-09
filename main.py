import emoji
import os

from aiogram import types
from keyboards.default import panel_choose_target, panel_choose_pack
from loader import bot, dp

user = 0

#старт
@dp.message_handler(commands=['start'])
async def hello(message: types.message):
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHL09ju_NYDBqyTq65N1BJqyacddxvSQACHxEAAowt_QcWMfHxvTZjli0E'),
    await message.answer('Привет! Я чат-бот который присылает что-то милое ' + emoji.emojize('🥰') + 'Кто будет этим счастивчиком?')
    await bot.send_message(message.chat.id, 'Кого мы будем радовать?', reply_markup=panel_choose_target)

#хочу привязать пользователя
@dp.message_handler(text='Хочу привязать пользователя')
async def chsv(message: types.message):
    #ожидание сообщения от пользователя
    await message.reply("Хорошо! Перешли мне сообщение от этого пупсика")
    get_id_forward(message)

async def get_id_forward(message: types.message):
    user = message.forward_from_chat.id
    await message.answer(f'Вот id пользователя: {user}!', reply_markup=panel_choose_pack)
    await folder_generator(user)

    

#функция для получения своего id 
@dp.message_handler(text='Хочу получать сам')
async def get_id_from_message(message: types.message):
    await message.answer('Хорошо! Получаю твой id ...' + emoji.emojize(' 🤔'))
    user = message.from_user.id

#функция для создания своей библиотеки
@dp.message_handler(text='Хочу использовать готовую библиотеку')
async def get_id_from_message(message: types.message):
    await message.answer('Хорошо! Получаю твой id ...' + emoji.emojize(' 🤔'))
    user = message.from_user.id
    await message.answer(f'Вот твой id: {user}!', reply_markup=panel_choose_target)
    await folder_generator(user)

#функция для получения id пользователя 


    

#функция создает папку с именем пользователя в директории data
async def folder_generator(user):
    os.mkdir("./data/{}".format(user))
    


async def start():
    await dp.start_polling(bot)


