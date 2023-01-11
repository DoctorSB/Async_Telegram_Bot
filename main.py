import emoji
import os

from aiogram import types
from aiogram.dispatcher .filters .state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from keyboards.default import panel_choose_target, panel_choose_pack, cancel_panel
from settings.loader import bot, dp
from settings.state import BotState

user = 0

# старт


@dp.message_handler(commands=['start'])
async def hello(message: types.Message) -> None:
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHL09ju_NYDBqyTq65N1BJqyacddxvSQACHxEAAowt_QcWMfHxvTZjli0E'),
    await message.answer('Привет! Я чат-бот который присылает что-то милое ' + emoji.emojize('🥰') + 'Кто будет этим счастивчиком?')
    await bot.send_message(message.chat.id, 'Кого мы будем радовать?', reply_markup=panel_choose_target)

# отмена


@dp.message_handler(text='Отмена')
async def cancel(state: FSMContext) -> None:
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()

# хочу привязать пользователя


@dp.message_handler(text='Хочу привязать пользователя', state=None)
async def chsv(message: types.Message) -> None:
    await BotState.forwarding.set()
    await message.answer("Хорошо! Перешли мне сообщение от этого пупсика", reply_markup=cancel_panel)

# получение id пользователя


@dp.message_handler(state=BotState.forwarding, content_types=types.ContentTypes.ANY)
async def get_id_from_forward(message: types.message, state: FSMContext):
    try:
        user = message.forward_from.id
    except AttributeError:
        if 'forward_sender_name' in message:
            await message.answer('Это анонимный пользователь')
            return  
        await message.answer('Это не пересланное сообщение')
        return
    print(message)
    async with state.proxy() as data:
        data ['id'] = message.forward_from.id
        user = data['id']
    await message.answer(user)
    await folder_generator(user)
    print(user, BotState.forwarding, BotState.on_other)

# функция для получения своего id


@dp.message_handler(text='Хочу получать сам')
async def get_id_from_user(message: types.message):
    await message.answer('Хорошо! Получаю твой id ...' + emoji.emojize(' 🤔'))
    user = message.from_user.id
    await message.answer(f'Вот твой id: {user}!', reply_markup=panel_choose_target)
    print(message)

# функция для создания своей библиотеки
# @dp.message_handler(text='Хочу использовать готовую библиотеку')
# async def get_id_from_message(message: types.message):
#     await message.answer('Отлично' + emoji.emojize(' 🤔'))
#     user = message.from_user.id
#     await message.answer(f'Вот твой id: {user}!', reply_markup=panel_choose_target)
#     await folder_generator(user)

# функция создает папку с именем пользователя в директории data


async def folder_generator(user):
    os.mkdir("./data/{}".format(user))


async def start():
    await dp.start_polling(bot)
