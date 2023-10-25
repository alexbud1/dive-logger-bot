from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from caching.cache_language import LanguageCache
from utils import get_phrase, get_profile_api
from keyboards.keyboards import (
    create_my_profile_keyboard,
    create_fill_profile_main_manu_keyboard,
    create_settings_keyboard,
    create_support_keyboard,
    create_dives_keyboard
)
from handlers.states import (
    Settings
)

router = Router()


# handle Dives button from main menu
@router.message(F.text.startswith("🐠"))
async def handle_dives_button(message: Message) -> None:
    await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "dives"), reply_markup=create_dives_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())


# handle Equipment button from main menu
@router.message(F.text.startswith("🤿"))
async def handle_equipment_button(message: Message) -> None:
    await message.answer("Section is not ready yet")


# handle Dive sites button from main menu
@router.message(F.text.startswith("🌍"))
async def handle_dive_sites_button(message: Message) -> None:
    await message.answer("Section is not ready yet")


# handle Tips and guides button from main menu
@router.message(F.text.startswith("📚"))
async def handle_tips_and_guides_button(message: Message) -> None:
    await message.answer("Section is not ready yet")


# handle Profile button from main menu
@router.message(F.text.startswith("👤"))
async def handle_profile_button(message: Message) -> None:

    user_profile = await get_profile_api(message.from_user.id, message=message)
    language = await LanguageCache.get_user_language(message.from_user.id)

    if type(user_profile) is dict:

        # fill profile text by components for registered user
        name = f"{get_phrase(language, 'profile_caption_name').replace('{name}', user_profile['name'])}"
        is_diver = f"{get_phrase(language, 'profile_caption_is_diver').replace('{is_diver}', '✅' if user_profile['is_diver'] else '❌')}"
        amount_of_dives = f"{get_phrase(language, 'profile_caption_amount_of_dives').replace('{amount_of_dives}', str(user_profile['amount_of_dives'])) if user_profile['amount_of_dives'] else ''}"
        country = f"{get_phrase(language, 'profile_caption_country').replace('{country}', user_profile['country']) if user_profile['country'] else ''}"
        profile_text = f"{name}{is_diver}{amount_of_dives}{country}"

        if user_profile["profile_photo"]:
            photo_url = user_profile["profile_photo"]
            await message.answer_photo(photo_url, caption=profile_text, reply_markup=create_my_profile_keyboard(language).as_markup())
        else:
            await message.answer(profile_text, reply_markup=create_my_profile_keyboard(language).as_markup())


    elif type(user_profile) is str:
        await message.answer(get_phrase(language, "profile_not_found"), reply_markup=create_fill_profile_main_manu_keyboard(language).as_markup())
    else:
        await message.answer("Unexpected error")


# handle Settings button from main menu
@router.message(F.text.startswith("⚙️"))
async def handle_settings_button(message: Message, state: FSMContext) -> None:
    await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "settings"), reply_markup=create_settings_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
    await state.set_state(Settings.language)


# handle Support button from main menu
@router.message(F.text.startswith("📞"))
async def handle_support_button(message: Message) -> None:
    await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "support"), reply_markup=create_support_keyboard(await LanguageCache.get_user_language(message.from_user.id)).as_markup())
