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

router = Router()

# handle next button from carousel keyboard
@router.callback_query(F.data.endswith('_dive'))
async def handle_next_dive(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()

    # update current page in state data
    state_data = await state.get_data()
    page = state_data["page"]

    # define whether user pressed next or previous button
    f_data = callback.data
    if f_data == 'next_dive':
        page -= 1
    elif f_data == 'previous_dive':
        page += 1
    await state.update_data(page=page)

    # get dives from api
    response = await get_dive_api(callback.from_user.id, page=page, size=1, callback=callback)

    pages_count = response['pages']
    dive = response['items'][0]

    carousel_keyboard = create_carousel_keyboard(await LanguageCache.get_user_language(callback.from_user.id), page, pages_count)
    
    await callback.message.delete()
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), "dive_message").format(max_depth = dive['max_depth'], duration = dive['duration'], water_temperature = dive['water_temperature'], date = dive['date'], location = dive['location'], visibility = dive['visibility'], dive_type = dive['dive_type'], dive_center = dive['dive_center'], dive_buddy = dive['dive_buddy'], description = dive['description'], wetsuit_type = dive['wetsuit_type'], wetsuit_thickness = dive['wetsuit_thickness'], weight = dive['weight'], air_temperature = dive['air_temperature'], air_pressure = dive['air_pressure'], current = dive['current'], dive_number = dive['dive_number']), reply_markup=carousel_keyboard.as_markup())
    await callback.answer()