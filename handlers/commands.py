from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from keyboards.keyboards import language_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! Please choose your prefered language:", reply_markup=language_keyboard.as_markup())
