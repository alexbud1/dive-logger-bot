from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from caching.cache_language import LanguageCache
from utils import get_phrase, get_dive_api
from datetime import datetime
from keyboards.keyboards import (
    create_back_to_dives_keyboard,
    create_dives_keyboard,
    create_carousel_keyboard
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

# handle dive logbook button from dive message menu
@router.callback_query(F.data.startswith('dive_logbook'))
async def handle_dive_logbook(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    # deal with pagination in state data
    state_data = await state.get_data()
    if "page" in state_data:
        page = state_data["page"]
    else:
        page = 1
        await state.update_data(page=page)


    response = await get_dive_api(callback.from_user.id, page=page, size=1, callback=callback)

    # if no dives found
    if response == 'not_found':
        await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "no_dives"), reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(callback.from_user.id)).as_markup())
        await callback.answer()
        return
    
    pages_count = response['pages']
    dive = response['items'][0]
    
    carousel_keyboard = create_carousel_keyboard(await LanguageCache.get_user_language(callback.from_user.id), page, pages_count)

    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "dive_message").format(max_depth = dive['max_depth'], duration = dive['duration'], water_temperature = dive['water_temperature'], date = dive['date'], location = dive['location'], visibility = dive['visibility'], dive_type = dive['dive_type'], dive_center = dive['dive_center'], dive_buddy = dive['dive_buddy'], description = dive['description'], wetsuit_type = dive['wetsuit_type'], wetsuit_thickness = dive['wetsuit_thickness'], weight = dive['weight'], air_temperature = dive['air_temperature'], air_pressure = dive['air_pressure'], current = dive['current'], dive_number = dive['dive_number']), reply_markup=carousel_keyboard.as_markup())
    await callback.answer()

