from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from caching.cache_language import LanguageCache
from handlers.states import EditProfile
from keyboards.keyboards import (create_main_menu_keyboard,
                                 create_send_coordinates_keyboard,
                                 create_skip_profile_photo_keyboard,
                                 is_diver_keyboard,
                                 create_edit_profile_keyboard,)
from utils import (create_profile_api, get_country_from_coordinates,
                   get_phrase, is_valid_country_name, translate_to_en,
                   update_profile_api)

router = Router()
import regex as re

# handle name entered by user for his profile
@router.message(EditProfile.name)
async def process_name(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\p{L} -]+$', message.text, re.UNICODE):
        if len(message.text)>=3 and len(message.text)<=100:
            await update_profile_api(message.from_user.id, "name", message.text, message=message)
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "name_saved"))
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "edit_profile_message"), reply_markup=create_edit_profile_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
            await state.clear()
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_name_length"))
            await state.set_state(EditProfile.name)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_name"))
        await state.set_state(EditProfile.name)

# handle amount of dives entered by user for editing his profile
@router.message(EditProfile.amount_of_dives)
async def process_amount_of_dives(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        if int(message.text)>=0 and int(message.text)<=20000:
            await update_profile_api(message.from_user.id, "amount_of_dives", int(message.text), message=message)
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "amount_of_dives_saved"))
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "edit_profile_message"), reply_markup=create_edit_profile_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
            await state.clear()
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_amount_of_dives"))
            await state.set_state(EditProfile.amount_of_dives)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "not_digit"))
        await state.set_state(EditProfile.amount_of_dives)

# handle country entered by user for editing his profile
# handle back to edit profile from country
@router.message(F.text.contains("🔙"), EditProfile.country)
async def process_skip_country(message: Message, state: FSMContext) -> None:
    if message.text == get_phrase(await LanguageCache.get_user_language(message.from_user.id), "back"):
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "edit_profile_message"), reply_markup=create_edit_profile_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
        await state.clear()

@router.message(EditProfile.country)
async def process_country(message: Message, state: FSMContext) -> None:
    if not message.location and is_valid_country_name(message.text):
        await update_profile_api(message.from_user.id, "country", message.text, message=message)
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "country_saved"))
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "edit_profile_message"), reply_markup=create_edit_profile_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
        await state.clear()
    elif message.location:
        country = get_country_from_coordinates(message.location.latitude, message.location.longitude)
        await update_profile_api(message.from_user.id, "country", country, message=message) 
        reply_markup = types.ReplyKeyboardRemove()
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "your_country"), reply_markup=reply_markup)
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "edit_profile_message"), reply_markup=create_edit_profile_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
        await state.clear()
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "not_country"))
        await state.set_state(EditProfile.country)

# handle profile photo entered by user for editing his profile
@router.message(EditProfile.profile_photo)
async def process_profile_photo(message: Message, state: FSMContext) -> None:
    MAX_FILE_SIZE_BYTES = 4 * 1024 * 1024 # 4 MB
    if message.media_group_id:
        data = await state.get_data()
        once = True if "once" not in data else False
        if once:
            await state.update_data(once=True)
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "photo_only_one"))
            await state.set_state(EditProfile.profile_photo)   
    
    # validate if its photo
    elif message.photo is None:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "not_photo"))
        await state.set_state(EditProfile.profile_photo)
    
    # 4MB limit
    elif message.photo[-1].file_size > MAX_FILE_SIZE_BYTES:
        print("photo too big")
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "photo_too_big"))
        await state.set_state(EditProfile.profile_photo)

    # if everything is ok
    elif message.photo:
        await update_profile_api(message.from_user.id, "profile_photo", message.photo[-1].file_id, message=message)
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "profile_photo_saved"))
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "edit_profile_message"), reply_markup=create_edit_profile_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
        await state.clear()
