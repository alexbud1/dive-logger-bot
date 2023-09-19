from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from caching.cache_language import LanguageCache
from utils import get_phrase
from keyboards.keyboards import (
    create_welcome_message_keyboard,
    create_skip_profile_photo_keyboard,
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
    await callback.message.edit_text(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "fill_profile_message"))
    await callback.answer()
    await state.set_state(FillProfile.name)

# handle callback from skipping filling profile
@router.callback_query(F.data.startswith('skip_filling_profile'))
async def handle_skip_filling_profile(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "skip_filling_profile_message"))
    await callback.answer()
    await state.set_state('free')

# handle callback from is_diver question
@router.callback_query(F.data.startswith('is_diver_'))
async def handle_is_diver(callback: types.CallbackQuery, state: FSMContext):
    is_diver = True if callback.data == 'is_diver_yes' else False
    await state.update_data(is_diver=is_diver)

    # for diver we proceed with amount of dives and for non diver - it is unnecessary, so we go to profile photo
    if is_diver:
        await state.set_state(FillProfile.amount_of_dives)
        phrase = get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "amount_of_dives")
        await callback.message.edit_text(phrase)
    else:
        await state.set_state(FillProfile.profile_photo)
        phrase = get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "profile_photo")
        skip_profile_photo_keyboard = create_skip_profile_photo_keyboard(await LanguageCache.get_user_language(callback.from_user.id))
        await callback.message.edit_text(phrase, reply_markup=skip_profile_photo_keyboard.as_markup())
    
    await callback.answer()

# handle callback from skipping profile photo
@router.callback_query(F.data.startswith('skip_profile_photo'))
async def handle_skip_profile_photo(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state('free')
    await callback.message.edit_text(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "signup_completed"))
    await callback.answer()
    data = await state.get_data()
    await callback.message.answer(str(data))
    await state.clear()