from environs import Env, EnvValidationError
import os

env = Env()
env.read_env()


def get_bot_token():
    try:
        BOT_TOKEN = env.str("BOT_TOKEN")
    except EnvValidationError:
        BOT_TOKEN = os.environ['BOT_TOKEN']
    return BOT_TOKEN


def get_admins():
    try:
        ADMINS = env.list("ADMINS")
    except EnvValidationError:
        ADMINS = os.environ['ADMINS'].split(',')
    return [int(id) for id in ADMINS]


BOT_TOKEN = get_bot_token()
ADMINS = get_admins()
