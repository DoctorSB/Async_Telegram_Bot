if __name__ == '__main__':
    from aiogram import executor
    from settings.loader import dp
    from main import on_startup

    print('бот запущен')
    executor.start_polling(dp, on_startup=on_startup)
