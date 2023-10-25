from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from caching.cache_language import LanguageCache
from utils import get_phrase
from datetime import datetime
from keyboards.keyboards import (
    create_back_to_dives_keyboard,
    create_dives_keyboard
)
from handlers.states import AddDive

router = Router()

# handle Add dive button from dive message menu
@router.callback_query(F.data.startswith('add_dive'))
async def handle_add_dive(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "add_dive_message"), reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
    await callback.answer()
    await state.set_state(AddDive.max_depth)

# hadnle back button from add dive message menu
@router.callback_query(F.data.startswith('back_to_dives'))
async def handle_back_to_dives(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "dives"), reply_markup=create_dives_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
    await callback.answer()
    await state.clear()

# handle today button from add dive message menu
@router.callback_query(F.data.startswith('today'), AddDive.date)
async def handle_today(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    today_date = datetime.now().strftime('%d.%m.%Y')

    await state.update_data(date=today_date)
    await state.set_state(AddDive.location)

    phrase = get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "location")
    await callback.message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
    await callback.answer()