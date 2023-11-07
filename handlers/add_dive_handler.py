from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from caching.cache_language import LanguageCache
from handlers.states import AddDive
import regex as re
from keyboards.keyboards import (
    create_back_to_dives_keyboard,
    create_today_keyboard,
    create_dives_keyboard
)
from utils import (
    get_phrase,
    is_valid_date,
    create_dive_api
)

router = Router()


#handle max depth entered by user for his dive
@router.message(AddDive.max_depth)
async def process_max_depth(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\d.,]+$', message.text): # check if its number, comma or dot
        depth = float(message.text if '.' in message.text else message.text.replace(',', '.')) # replace comma with dot if its comma

        if depth>=0 and depth<=350:
            await state.update_data(max_depth=message.text)
            await state.set_state(AddDive.duration)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "duration")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())    
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_max_depth"))
            await state.set_state(AddDive.max_depth)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_max_depth"))
        await state.set_state(AddDive.max_depth)

#handle duration entered by user for his dive
@router.message(AddDive.duration)
async def process_duration(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\d.,]+$', message.text): # check if its number, comma or dot

        duration = float(message.text if '.' in message.text else message.text.replace(',', '.')) # replace comma with dot if its comma
        if duration>=0 and duration<=6000:
            await state.update_data(duration=message.text)
            await state.set_state(AddDive.gas)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "gas")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())    
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_duration"))
            await state.set_state(AddDive.duration)

    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_duration"))
        await state.set_state(AddDive.duration)

#handle water temperature entered by user for his dive
@router.message(AddDive.water_temperature)
async def process_water_temperature(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\d.,-]+$', message.text): # check if its number, comma or dot

        water_temperature = float(message.text if '.' in message.text else message.text.replace(',', '.'))  # replace comma with dot if its comma
        if water_temperature>=-40 and water_temperature<=40:
            await state.update_data(water_temperature=message.text)
            await state.set_state(AddDive.air_temperature)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "air_temperature")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())    
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_water_temperature"))
            await state.set_state(AddDive.water_temperature)

    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_water_temperature"))
        await state.set_state(AddDive.water_temperature)

# handle date entered by user for his dive
@router.message(AddDive.date)
async def process_date(message: Message, state: FSMContext) -> None:
    if is_valid_date(message.text):
        await state.update_data(date=message.text)
        await state.set_state(AddDive.location)

        phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "location")
        await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_date"))
        await state.set_state(AddDive.date)

# handle location entered by user for his dive
@router.message(AddDive.location)
async def process_location(message: Message, state: FSMContext) -> None:
    if len(message.text) <= 150:
        await state.update_data(location=message.text)
        await state.set_state(AddDive.dive_center)

        phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "dive_center")
        await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_location"))
        await state.set_state(AddDive.location)

# handle visibility entered by user for his dive
@router.message(AddDive.visibility)
async def process_visibility(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\p{L} -]+$', message.text, re.UNICODE):
        if len(message.text) <= 50:
            await state.update_data(visibility=message.text)
            await state.set_state(AddDive.current)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "current")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_visibility"))
            await state.set_state(AddDive.visibility)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_visibility"))
        await state.set_state(AddDive.visibility)

# handle dive type entered by user for his dive
@router.message(AddDive.dive_type)
async def process_dive_type(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\p{L} -]+$', message.text, re.UNICODE):
        if len(message.text) <= 50:
            await state.update_data(dive_type=message.text)
            await state.set_state(AddDive.water_temperature)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "water_temperature")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_dive_type"))
            await state.set_state(AddDive.dive_type)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_dive_type"))
        await state.set_state(AddDive.dive_type)

# handle dive center entered by user for his dive
@router.message(AddDive.dive_center)
async def process_dive_center(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\p{L} -]+$', message.text, re.UNICODE):
        if len(message.text) <= 150:
            await state.update_data(dive_center=message.text)
            await state.set_state(AddDive.max_depth)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "max_depth")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
            
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_dive_center"))
            await state.set_state(AddDive.dive_center)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_dive_center"))
        await state.set_state(AddDive.dive_center)

# handle dive buddy entered by user for his dive
@router.message(AddDive.dive_buddy)
async def process_dive_buddy(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\p{L} -]+$', message.text, re.UNICODE):
        if len(message.text) <= 150:
            await state.update_data(dive_buddy=message.text)
            await state.set_state(AddDive.description)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "description")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_dive_buddy"))
            await state.set_state(AddDive.dive_buddy)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_dive_buddy"))
        await state.set_state(AddDive.dive_buddy)

# handle description entered by user for his dive
@router.message(AddDive.description)
async def process_description(message: Message, state: FSMContext) -> None:
    if len(message.text) <= 800:
        await state.update_data(description=message.text)

        info = await state.get_data()
        info["telegram_id"] = message.from_user.id

        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "dive_saved"))   

        if await create_dive_api(info, message=message):
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "dives"), reply_markup=create_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
            await state.set_state('free')
            await state.clear() 

    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_description"))
        await state.set_state(AddDive.description)

# handle wetsuit type entered by user for his dive
@router.message(AddDive.wetsuit_type)
async def process_wetsuit_type(message: Message, state: FSMContext) -> None:
    if len(message.text) <= 70:
        await state.update_data(wetsuit_type=message.text)
        await state.set_state(AddDive.wetsuit_thickness)

        phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "wetsuit_thickness")
        await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_wetsuit_type"))
        await state.set_state(AddDive.wetsuit_type)

# handle wetsuit thickness entered by user for his dive
@router.message(AddDive.wetsuit_thickness)
async def process_wetsuit_thickness(message: Message, state: FSMContext) -> None:
    if len(message.text) <= 50:
        await state.update_data(wetsuit_thickness=message.text)
        await state.set_state(AddDive.weight)

        phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "weight")
        await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_wetsuit_thickness"))
        await state.set_state(AddDive.wetsuit_thickness)

# handle weight entered by user for his dive
@router.message(AddDive.weight)
async def process_weight(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\d.,]+$', message.text):
        weight = float(message.text if '.' in message.text else message.text.replace(',', '.'))

        if weight>=0 and weight<=50:
            await state.update_data(weight=message.text)
            await state.set_state(AddDive.dive_buddy)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "dive_buddy")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())    
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_weight"))
            await state.set_state(AddDive.weight)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_weight"))
        await state.set_state(AddDive.weight)

# handle air temperature entered by user for his dive
@router.message(AddDive.air_temperature)
async def process_air_temperature(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\d.,-]+$', message.text):
        air_temperature = float(message.text if '.' in message.text else message.text.replace(',', '.'))

        if air_temperature>=-50 and air_temperature<=50:
            await state.update_data(air_temperature=message.text)
            await state.set_state(AddDive.air_pressure)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "air_pressure")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())    
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_air_temperature"))
            await state.set_state(AddDive.air_temperature)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_air_temperature"))
        await state.set_state(AddDive.air_temperature)

# handle air pressure entered by user for his dive
@router.message(AddDive.air_pressure)
async def process_air_pressure(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\d.,-]+$', message.text):
        air_pressure = float(message.text if '.' in message.text else message.text.replace(',', '.'))

        if air_pressure>=0 and air_pressure<=2000:
            await state.update_data(air_pressure=message.text)
            await state.set_state(AddDive.visibility)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "visibility")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())    
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_air_pressure"))
            await state.set_state(AddDive.air_pressure)
    else:   
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_air_pressure"))
        await state.set_state(AddDive.air_pressure)

# handle current entered by user for his dive
@router.message(AddDive.current)
async def process_current(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\p{L} -]+$', message.text, re.UNICODE):
        if len(message.text) <= 50:
            await state.update_data(current=message.text)
            await state.set_state(AddDive.wetsuit_type)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "wetsuit_type")
            await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_current"))
            await state.set_state(AddDive.current)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_current"))
        await state.set_state(AddDive.current)

# handle dive number entered by user for his dive
@router.message(AddDive.dive_number)
async def process_dive_number(message: Message, state: FSMContext) -> None:
    if re.match(r'^[\d.,]+$', message.text):
        dive_number = float(message.text if '.' in message.text else message.text.replace(',', '.'))

        if dive_number>=1 and dive_number<=20000:
            # await state.update_data(dive_number=message.text)
            # info = await state.get_data()
            # info["telegram_id"] = message.from_user.id

            # await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "dive_saved"))   

            # if await create_dive_api(info, message=message):
            #     await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "dives"), reply_markup=create_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
            #     await state.set_state('free')
            #     await state.clear()    
            await state.update_data(dive_number=message.text)
            await state.set_state(AddDive.date)

            phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "date")
            await message.answer(phrase, reply_markup=create_today_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())    

        else:
            await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_dive_number"))
            await state.set_state(AddDive.dive_number)
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_dive_number"))
        await state.set_state(AddDive.dive_number)

# handle gas entered by user for his dive
@router.message(AddDive.gas)
async def process_gas(message: Message, state: FSMContext) -> None:
    if len(message.text) <= 150:
        await state.update_data(gas=message.text)
        await state.set_state(AddDive.dive_type)

        phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "dive_type")
        await message.answer(phrase, reply_markup=create_back_to_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
    else:
        await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "invalid_gas"))
        await state.set_state(AddDive.gas)