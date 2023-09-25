from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from caching.cache_language import LanguageCache
from handlers.states import FillProfile
from keyboards.keyboards import (create_main_menu_keyboard,
                                 create_send_coordinates_keyboard,
                                 create_skip_profile_photo_keyboard,
                                 is_diver_keyboard)
from utils import (create_profile_api, get_country_from_coordinates,
                   get_phrase, is_valid_country_name, translate_to_en)

router = Router()
import regex as re


# handle name entered by user for his profile
@router.message(FillProfile.name)
async def process_name(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\p{L} -]+$', message.text, re.UNICODE):
        if len(message.text)>=3 and len(message.text)<=100:
            await state.update_data(name=message.text)
            await state.set_state(FillProfile.is_diver)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "is_diver").replace("{name}", message.text)
            await message.answer(phrase, reply_markup=is_diver_keyboard.as_markup())    
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_name_length"))
            await state.set_state(FillProfile.name)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_name"))
        await state.set_state(FillProfile.name)

# handle photo entered by user for his profile
@router.message(FillProfile.profile_photo)
async def process_profile_photo(message: Message, state: FSMContext) -> None:
    MAX_FILE_SIZE_BYTES = 4 * 1024 * 1024 # 4 MB
    if message.media_group_id:
        data = await state.get_data()
        once = True if "once" not in data else False
        if once:
            await state.update_data(once=True)
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "photo_only_one"))
            await state.set_state(FillProfile.profile_photo)    
        
            
    # validate if its photo
    elif message.photo is None:
        print("not photo")
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "not_photo"))
        await state.set_state(FillProfile.profile_photo)
    # 4MB limit
    elif message.photo[-1].file_size > MAX_FILE_SIZE_BYTES:
        print("photo too big")
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "photo_too_big"))
        await state.set_state(FillProfile.profile_photo)
    # if everything is ok
    elif message.photo:
        await state.update_data(profile_photo=message.photo[-1].file_id)
        data = await state.get_data()
        data["telegram_id"] = message.from_user.id
        await message.answer(str(data))

        if await create_profile_api(data, message=message):

            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "signup_completed"))
            await welcome_to_main_menu(message)
            
            await state.set_state('free')
            await state.clear()

# handle amount of dives entered by user for his profile
@router.message(FillProfile.amount_of_dives)
async def process_amount_of_dives(message: Message, state: FSMContext) -> None:

    # validate if its digit
    if not message.text or not message.text.isdigit():
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "not_digit"))
        await state.set_state(FillProfile.amount_of_dives)
    elif int(message.text) < 0 or int(message.text) > 20000:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_amount_of_dives"))
        await state.set_state(FillProfile.amount_of_dives)
    else:
        await state.update_data(amount_of_dives=message.text)
        await state.set_state(FillProfile.country)
        send_coordinates_keyboard = create_send_coordinates_keyboard(await LanguageCache.get_user_language(message.from_user.id))
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "country"), reply_markup=send_coordinates_keyboard.as_markup(resize_keyboard=True))


# handle skip country 
@router.message(F.text.contains("🔄"), FillProfile.country)
async def process_skip_country(message: Message, state: FSMContext) -> None:
    if message.text == get_phrase(await LanguageCache.get_user_language(message.from_user.id), "skip_button"):
        await state.update_data(country=None)
        await state.set_state(FillProfile.profile_photo)
        reply_markup = types.ReplyKeyboardRemove()
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "profile_photo"), reply_markup=reply_markup)


# handle country entered by user for his profile
@router.message(FillProfile.country)
async def process_country(message: Message, state: FSMContext) -> None:
    print(message.location)
    skip_profile_photo_keyboard = create_skip_profile_photo_keyboard(await LanguageCache.get_user_language(message.from_user.id))
    if not message.location and is_valid_country_name(message.text):
        await state.update_data(country=translate_to_en(message.text))
        await state.set_state(FillProfile.profile_photo)
        reply_markup = types.ReplyKeyboardRemove()
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "your_country"), reply_markup=reply_markup)
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "profile_photo"), reply_markup=skip_profile_photo_keyboard.as_markup())
    elif message.location:
        country = get_country_from_coordinates(message.location.latitude, message.location.longitude)
        await state.update_data(country=country)
        reply_markup = types.ReplyKeyboardRemove()
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "your_country"), reply_markup=reply_markup)
        await state.set_state(FillProfile.profile_photo)
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "profile_photo"), reply_markup=skip_profile_photo_keyboard.as_markup())
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "not_country"))
        await state.set_state(FillProfile.country)

async def welcome_to_main_menu(message: Message) -> None:
    main_menu_keyboard = await create_main_menu_keyboard(await LanguageCache.get_user_language(message.from_user.id), message)
    await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "main_menu"), reply_markup=main_menu_keyboard.as_markup(resize_keyboard=True))

