from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from caching.cache_language import LanguageCache
from utils import get_phrase
from keyboards.keyboards import (
    create_welcome_message_keyboard
)
from handlers.states import FillProfile
router = Router()


# handle callback from language choice
@router.callback_query(F.data.startswith('lang_'))
async def handle_language_choice(callback: types.CallbackQuery):

    old_language = await LanguageCache.get_user_language(callback.from_user.id)
    new_language = callback.data

    if old_language == new_language:
        await callback.answer(get_phrase(new_language, "language_already_chosen"), show_alert=True)
    else:
        try:
            await LanguageCache.set_user_language(callback.from_user.id, new_language)
        except Exception as e:

            if "User settings not modified" in str(e):
                await callback.message.edit_text(get_phrase(new_language, "language_changed"))
            else:
                await callback.message.edit_text(get_phrase("lang_en", "unexpected_error"))
                raise e

        await callback.message.edit_text(get_phrase(new_language, "language_changed"))
        await callback.answer()
        
        welcome_message_keyboard = create_welcome_message_keyboard(new_language)
        await callback.message.answer(get_phrase(new_language, "welcome_message"), reply_markup=welcome_message_keyboard.as_markup())

# handle callback from filling profile and starting filling profile state
@router.callback_query(F.data.startswith('fill_profile'))
async def handle_fill_profile(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "fill_profile_message"))
    await callback.answer()
    await state.set_state(FillProfile.name)