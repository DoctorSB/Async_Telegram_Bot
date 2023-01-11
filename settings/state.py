from aiogram.dispatcher.filters.state import StatesGroup, State

class BotState(StatesGroup):
    forwarding = State()
    on_other = State()
    