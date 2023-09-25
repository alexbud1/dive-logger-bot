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
    InlineKeyboardButton(text="Українська 🇺🇦", callback_data='lang_ukr')
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
    my_profile_keyboard.add(
        InlineKeyboardButton(text=get_phrase(language, "edit_profile"), callback_data='edit_profile'),
        InlineKeyboardButton(text=get_phrase(language, "back"), callback_data='back_my_profile')
    )
    return my_profile_keyboard