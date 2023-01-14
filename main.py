import emoji
import os

from aiogram import types, executor
from aiogram.dispatcher .filters .state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from keyboards.default import panel_choose_target, panel_choose_pack, cancel_panel
from settings.loader import bot, dp
from settings.state import other_State
from database.sqlite import db_start, create_profile, edit_profile

user = 0


# старт

async def on_startup(self):
    await db_start(self)


# стартовое сообщение

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
async def not_chsv(message: types.Message) -> None:
    await other_State.forwarding.set()
    await message.answer("Хорошо! Перешли мне сообщение от этого пупсика", reply_markup=cancel_panel)


# получение id пользователя


@dp.message_handler(state=other_State.forwarding, content_types=types.ContentTypes.ANY)
async def get_id_from_forward(message: types.message, state: FSMContext):
    try:
        global user
        user = message.forward_from.id
        await message.answer('Отлично' + emoji.emojize(' 🤔'), reply_markup=panel_choose_pack)
    except AttributeError:
        if 'forward_sender_name' in message:
            await message.answer('Это анонимный пользователь')
            return
        await message.answer('Это не пересланное сообщение')
        return
    await create_profile(user_id=user)
    await message.answer(user)
    await folder_generator(user)
    await state.finish()

# функция для получения своего id


@dp.message_handler(text='Хочу получать сам')
async def get_id_from_user(message: types.message):
    await message.answer('Хорошо! Получаю твой id ...' + emoji.emojize(' 🤔'))
    global user
    user = message.from_user.id
    await create_profile(user_id=user)
    await message.answer(f'Вот твой id: {user}!', reply_markup=panel_choose_pack)
    await folder_generator(user)


@dp.message_handler(state=other_State.waiting, content_types=types.ContentTypes.ANY)
async def photo_add(message: types.message, state: FSMContext):
    print("photo_add\n")
    await message.photo[0].download('./data/{}/img/{}.jpg'.format(user, message.photo[0].file_unique_id))
    await message.answer('Фото добавлено в библиотеку')
    if message.text == 'Готово':
        await message.answer('Все фото добавлены в библиотеку', reply_markup=panel_choose_pack)
        other_State.work.set()

# запись фотографий в папку этого пользователя


# функция для создания своей библиотеки


@dp.message_handler(text='Соберу свою библиотеку')
async def get_id_from_message(message: types.message, state: FSMContext):
    await message.answer('Отлично' + emoji.emojize(' 🤔'), reply_markup=cancel_panel)
    await other_State.waiting.set()


# функция создает папку с именем пользователя в директории data


async def folder_generator(user):
    if not os.path.exists("./data/{}".format(user)):
        os.mkdir("./data/{}".format(user))
        os.mkdir("./data/{}/img".format(user))
