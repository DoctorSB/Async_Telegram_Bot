import sqlite3 as sq


async def db_start(self):
    global db, cursor

    db = sq.connect('db.db')
    cursor = db.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, send_text TEXT, img TEXT, stickers TEXT)")

    db.commit()


async def create_profile(user_id):
    user = cursor.execute(
        "SELECT * FROM profile WHERE user_id = '{key}'".format(key=user_id)).fetchone()
    if not user:
        cursor.execute("INSERT INTO profile VALUES (?, ?, ?, ?)",
                       (user_id, '', '', ''))
        db.commit()
        return True


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cursor.execute("UPDATE profile SET send_text = '{send_text}', img = '{img}', stickers = '{stickers}' WHERE user_id = '{user_id}'".format(
            send_text=data['send_text'], img=data['img'], stickers=data['stickers'], user_id=user_id))
        db.commit()
