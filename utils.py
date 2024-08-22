from DatabaseIO import DatabaseIO
import asyncio
from config import *

loop = asyncio.get_event_loop()

db = DatabaseIO(user=user,
                password=passwd,
                database=dbase,
                host=host,
                loop=loop)


async def update_state(text: str, bot, chat_id: int, user_message_id: int, bot_message_id: int, reply_markup=None):
    await bot.delete_message(chat_id=chat_id, message_id=user_message_id)
    await bot.edit_message_text(text=text, chat_id=chat_id,
                                message_id=bot_message_id, reply_markup=reply_markup)