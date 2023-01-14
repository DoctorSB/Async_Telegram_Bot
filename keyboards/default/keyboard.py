from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

panel_choose_target = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Хочу привязать пользователя'),
            KeyboardButton(text='Хочу получать сам'),
        ],
    ],
    resize_keyboard=True
)

panel_choose_pack = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Хочу использовать готовую библиотеку'),
            KeyboardButton(text='Соберу свою библиотеку'),
        ],
    ],
    resize_keyboard=True
)

cancel_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отмена'),
        ],
    ],
    resize_keyboard=True
)
