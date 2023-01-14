from aiogram.dispatcher.filters.state import StatesGroup, State


class other_State(StatesGroup):
    forwarding = State()
    waiting = State()
    work = State()
