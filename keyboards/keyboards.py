from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
import json
from utils import get_phrase


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