import json

from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from utils import get_phrase, get_profile_api

language_keyboard = InlineKeyboardBuilder()
language_keyboard.add(
    InlineKeyboardButton(text="English 🇺🇸", callback_data='lang_en'),
    InlineKeyboardButton(text="🇺🇦 Українська", callback_data='lang_ukr')
)

settings_language_keyboard = InlineKeyboardBuilder()
settings_language_keyboard.add(
    InlineKeyboardButton(text="English 🇺🇸", callback_data='lang_en_settings'),
    InlineKeyboardButton(text="🇺🇦 Українська", callback_data='lang_ukr_settings')
)

def create_welcome_message_keyboard(language: str) -> InlineKeyboardBuilder:
    welcome_message_keyboard = InlineKeyboardBuilder()
    welcome_message_keyboard.add(
        InlineKeyboardButton(text=get_phrase(language, "fill_profile"), callback_data='fill_profile'),
        InlineKeyboardButton(text=get_phrase(language, "skip_button"), callback_data='skip_filling_profile')
    )
    return welcome_message_keyboard


is_diver_keyboard = InlineKeyboardBuilder()
is_diver_keyboard.add(
    InlineKeyboardButton(text='✅', callback_data='is_diver_yes'),
    InlineKeyboardButton(text='❌', callback_data='is_diver_no')
)
def create_skip_profile_photo_keyboard(language: str) -> InlineKeyboardBuilder:
    skip_profile_photo_keyboard = InlineKeyboardBuilder()
    skip_profile_photo_keyboard.add(
        InlineKeyboardButton(text=get_phrase(language, "skip_button"), callback_data='skip_profile_photo')
    )
    return skip_profile_photo_keyboard

def create_send_coordinates_keyboard(language: str) -> ReplyKeyboardBuilder:
    send_coordinates_keyboard = ReplyKeyboardBuilder()
    send_coordinates_keyboard.row(
        types.KeyboardButton(text=get_phrase(language, "send_coordinates_button"), request_location=True),
        types.KeyboardButton(text=get_phrase(language, "skip_button"))
    )
    return send_coordinates_keyboard

async def create_main_menu_keyboard(language: str, message: Message = None, callback: types.CallbackQuery = None) -> ReplyKeyboardBuilder:
    main_menu_keyboard = ReplyKeyboardBuilder()

    response = await get_profile_api(message.from_user.id, message=message) if message else await get_profile_api(callback.from_user.id, callback=callback)
    if type(response) is dict:
        main_menu_keyboard.row(
            types.KeyboardButton(text=get_phrase(language, "dives_button")),
            types.KeyboardButton(text=get_phrase(language, "equipment_button"))
        )

    main_menu_keyboard.row(
        types.KeyboardButton(text=get_phrase(language, "dive_sites_button")),
        types.KeyboardButton(text=get_phrase(language, "tips_and_guides_button"))
    )
    main_menu_keyboard.row(
        types.KeyboardButton(text=get_phrase(language, "profile_button")),
        types.KeyboardButton(text=get_phrase(language, "settings_button"))
    )
    main_menu_keyboard.row(
        types.KeyboardButton(text=get_phrase(language, "support_button")),
    )
    return main_menu_keyboard

def create_my_profile_keyboard(language: str) -> InlineKeyboardBuilder:
    my_profile_keyboard = InlineKeyboardBuilder()
    my_profile_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "edit_profile"), callback_data='edit_profile'),
    )
    my_profile_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_menu')
    )
    return my_profile_keyboard

def create_fill_profile_main_manu_keyboard(language: str) -> InlineKeyboardBuilder:
    fill_profile_main_manu_keyboard = InlineKeyboardBuilder()
    fill_profile_main_manu_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "fill_profile"), callback_data='fill_profile'),
    )
    fill_profile_main_manu_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_menu')
    )
    return fill_profile_main_manu_keyboard

def create_settings_keyboard(language: str) -> InlineKeyboardBuilder:
    settings_keyboard = InlineKeyboardBuilder()
    settings_keyboard.add(
        InlineKeyboardButton(text=get_phrase(language, "language"), callback_data='language'),
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_menu')
    )
    return settings_keyboard

def create_edit_profile_keyboard(language: str) -> InlineKeyboardBuilder:
    edit_profile_keyboard = InlineKeyboardBuilder()
    edit_profile_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "name_button"), callback_data='edit_name'),
        InlineKeyboardButton(text=get_phrase(language, "diver_button"), callback_data='edit_is_diver')
    )
    edit_profile_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "amount_of_dives_button"), callback_data='edit_amount_of_dives'),
        InlineKeyboardButton(text=get_phrase(language, "country_button"), callback_data='edit_country')
    )
    edit_profile_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "profile_photo_button"), callback_data='edit_photo_profile'),
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_menu')
    )
    return edit_profile_keyboard

def create_back_to_edit_profile_keyboard(language: str) -> InlineKeyboardBuilder:
    back_to_edit_profile_keyboard = InlineKeyboardBuilder()
    back_to_edit_profile_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_edit_profile')
    )
    return back_to_edit_profile_keyboard

def create_is_diver_edit_profile_keyboard(language: str) -> InlineKeyboardBuilder:
    is_diver_edit_profile_keyboard = InlineKeyboardBuilder()
    is_diver_edit_profile_keyboard.row(
        InlineKeyboardButton(text='✅', callback_data='edit_is_diver_yes'),
        InlineKeyboardButton(text='❌', callback_data='edit_is_diver_no')
    )
    is_diver_edit_profile_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_edit_profile')
    )
    return is_diver_edit_profile_keyboard

def create_edit_country_keyboard(language: str) -> ReplyKeyboardBuilder:
    edit_country_keyboard = ReplyKeyboardBuilder()
    edit_country_keyboard.row(
        types.KeyboardButton(text=get_phrase(language, "send_coordinates_button"), request_location=True),
        types.KeyboardButton(text=get_phrase(language, "back"))
    )
    return edit_country_keyboard

def create_support_keyboard(language: str) -> InlineKeyboardBuilder:
    support_keyboard = InlineKeyboardBuilder()
    support_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "support_button"), callback_data='start_support')
    )
    support_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_menu')
    )
    return support_keyboard

def create_back_to_menu_keyboard(language: str) -> InlineKeyboardBuilder:
    back_to_menu_keyboard = InlineKeyboardBuilder()
    back_to_menu_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_menu')
    )
    return back_to_menu_keyboard

def create_dives_keyboard(language: str) -> InlineKeyboardBuilder:
    dives_keyboard = InlineKeyboardBuilder()
    dives_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "add_dive"), callback_data='add_dive'),
        InlineKeyboardButton(text=get_phrase(language, "dive_logbook"), callback_data='dive_logbook')
    )
    dives_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_menu')
    )
    return dives_keyboard

def create_back_to_dives_keyboard(language: str) -> InlineKeyboardBuilder:
    back_to_dives_keyboard = InlineKeyboardBuilder()
    back_to_dives_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_dives')
    )
    return back_to_dives_keyboard

def create_today_keyboard(language: str) -> InlineKeyboardBuilder:
    today_keyboard = InlineKeyboardBuilder()
    today_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "today_button"), callback_data='today')
    )
    today_keyboard.row(
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_to_dives')
    )
    return today_keyboard

def create_carousel_keyboard(language: str, page: int, pages_count: int) -> InlineKeyboardBuilder:
    carousel_keyboard = InlineKeyboardBuilder()
    print(f"page: {page}, pages_count: {pages_count}")
    # generate carousel keyboard
    if pages_count == 2 or (page == 1 and pages_count > 2):
        carousel_keyboard.add(
            types.InlineKeyboardButton(text=get_phrase(language, "previous"), callback_data="previous_dive")
        )
    elif (page == pages_count and pages_count > 2):
        carousel_keyboard.add(
            types.InlineKeyboardButton(text=get_phrase(language, "next"), callback_data="next_dive")
        )
    elif pages_count > 2:
        carousel_keyboard.add(
            types.InlineKeyboardButton(text=get_phrase(language, "previous"), callback_data="previous_dive"),
            types.InlineKeyboardButton(text=get_phrase(language, "next"), callback_data="next_dive")
        )

    return carousel_keyboard
