from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from caching.cache_language import LanguageCache
from aiogram.fsm.context import FSMContext
from database.config import user_settings
from handlers.fill_profile import welcome_to_main_menu
from keyboards.keyboards import (
    create_welcome_message_keyboard,
    language_keyboard
)
from utils import get_phrase, get_profile_api

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:

    # remove main_menu keyboard
    service_message = await message.answer("Loading...", reply_markup=types.ReplyKeyboardRemove())
    await service_message.delete()
    await state.clear()

    # Check if the user already has a language set
    language = await LanguageCache.get_user_language(message.from_user.id)

    if language is not None:
        response = await get_profile_api(message.from_user.id, message=message)

        # If the user has a language set and is not registered, send the main menu
        if type(response) is not dict and response:
            welcome_message_keyboard = create_welcome_message_keyboard(language)
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "welcome_message"), reply_markup=welcome_message_keyboard.as_markup())
        
        # send main_menu if user is registered and has a language set
        elif type(response) is dict:
            await welcome_to_main_menu(message)

    # If the user does not have a language set, send the language choice keyboard
    else:
        await message.answer("Hello! Please choose your prefered language:", reply_markup=language_keyboard.as_markup())