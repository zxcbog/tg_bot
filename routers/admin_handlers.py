from aiogram import Router
from utils import db
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import html
from .keyboards.keyboards import admin_keyboard_markup


router = Router()

admin_ids = db.tasks_handler("SELECT telegram_user_id FROM public.admins")


# @router.message(CommandStart(), lambda chat : msg.from_user.id in admin_ids)
# async def command_start_handler(message: Message) -> None:
#     await message.reply(f"Приветствую, {html.bold(message.from_user.full_name)}!\n", reply_markup=admin_keyboard_markup)
