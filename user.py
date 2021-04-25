import sqlite3
import sys

from aiogram import types

conn = sqlite3.connect("users.db")
cur = conn.cursor()


def createdb():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        userid INT PRIMARY KEY,
        lastfmusername TEXT,
        name TEXT
        );
    """)
    conn.commit()


def exists(user_id: int) -> bool:
    """
    check if user exists

    :param user_id: user's Telegram id
    :return: True if exists, False if not
    """
    result = cur.execute(f"""SELECT 1 FROM users WHERE userid = {user_id}""").fetchone()
    if result:
        return True
    else:
        return False


def register(user_id: int) -> bool:
    """
    register user

    :param userid: user's Telegram id
    :return: is operation successful
    """
    if exists(user_id):
        return False
    else:
        cur.execute("""INSERT INTO users VALUES (?, ?, ?)""", (user_id, None, None))
        conn.commit()
        return True


def delete(user_id: int) -> bool:
    cur.execute(f"""DELETE FROM users WHERE userid = {user_id}""")
    conn.commit()
    return True


def get_lastfm_username(user_id: int) -> str:
    cur.execute("SELECT lastfmusername FROM users WHERE userid = ?", [str(user_id)])
    return cur.fetchone()[0]


def get_name(user_id) -> str:
    cur.execute("SELECT name FROM users WHERE userid = ?", [str(user_id)])
    return cur.fetchone()[0]


def set_lastfm_username(user_id: int, username: str) -> bool:
    try:
        cur.execute("UPDATE users SET lastfmusername = ? WHERE userid = ?", (username, user_id))
        conn.commit()
        return True
    except:
        return False


def set_name(user_id: int, name: str) -> bool:
    try:
        cur.execute("UPDATE users SET name = ? WHERE userid = ?", (name, user_id))
        conn.commit()
        return True
    except:
        return False
