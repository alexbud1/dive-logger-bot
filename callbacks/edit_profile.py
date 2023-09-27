from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from caching.cache_language import LanguageCache
from utils import get_phrase, update_profile_api
from keyboards.keyboards import (
    create_edit_profile_keyboard,
    create_back_to_edit_profile_keyboard,
    create_is_diver_edit_profile_keyboard,
    create_edit_country_keyboard
)
from handlers.states import EditProfile

router = Router()


# handle callback from editing name
@router.callback_query(F.data.startswith('edit_name'))
async def handle_edit_name(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "edit_name"), reply_markup=create_back_to_edit_profile_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
    await callback.answer()
    await state.set_state(EditProfile.name)


# handle callback from choosing is_diver status
@router.callback_query(F.data.startswith('edit_is_diver_'), EditProfile.is_diver)
async def handle_is_diver(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    is_diver = True if callback.data.split("_")[2] == "yes" else False
    await update_profile_api(callback.from_user.id, "is_diver", is_diver, callback=callback)
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "is_diver_saved"))
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "edit_profile_message"), reply_markup=create_edit_profile_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
    await callback.answer()
    await state.clear()

# handle callback from editing is_diver
@router.callback_query(F.data.startswith('edit_is_diver'))
async def handle_edit_is_diver(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "edit_is_diver"), reply_markup=create_is_diver_edit_profile_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
    await callback.answer()
    await state.set_state(EditProfile.is_diver)

# handle callback from editing amount of dives
@router.callback_query(F.data.startswith('edit_amount_of_dives'))
async def handle_edit_amount_of_dives(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "edit_amount_of_dives"), reply_markup=create_back_to_edit_profile_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
    await callback.answer()
    await state.set_state(EditProfile.amount_of_dives)

# handle callback from editing country
@router.callback_query(F.data.startswith('edit_country'))
async def handle_edit_country(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "edit_country"), reply_markup=create_edit_country_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup(one_time_keyboard=True))
    await callback.answer()
    await state.set_state(EditProfile.country)

# handle callback from editing profile photo
@router.callback_query(F.data.startswith('edit_photo_profile'))
async def handle_edit_profile_photo(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "edit_profile_photo"), reply_markup=create_back_to_edit_profile_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
    await callback.answer()
    await state.set_state(EditProfile.profile_photo)

#handle callback from back to edit profile
@router.callback_query(F.data.startswith('back_to_edit_profile'))
async def handle_back_to_edit_profile(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "edit_profile_message"), reply_markup=create_edit_profile_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
    await callback.answer()
    await state.clear()