import os
from aiogram import types, Router, F
from aiogram.filters import (
    Command,
    or_f,
)  # 1 клас для обработки только команды старт, второй для всех. or_f - для написания дополнительных условий или через запятую
from aiogram.enums import ParseMode

from filters.chat_types import ChatTypeFilter

from kbds.reply import get_keyboard
from kbds.inline import get_inlineMix_btns
from texts_message import about_txt, start_page_txt, whereami_txt
from texts_message.commission_txt import (
    commission_txt1,
    commission_txt2,
    commission_txt3,
    commission_txt4,
)


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(
    (F.text.lower().contains("start")) | (F.text.lower().contains("меню"))
)
async def start_cmd(message: types.Message):
    await message.answer(
        start_page_txt.GREETINGS,
        reply_markup=get_keyboard(
            "О МТУСИ",
            "Как добраться",
            "Приёмная комиссия",
            "Общежитие",
            "Обратная связь",
            placeholder="Что Вас интересует?",
            sizes=(2, 2),
        ),
    )

@user_private_router.message(F.text.lower() == "о мтуси")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer(
        about_txt.about_mtuci,
        reply_markup=get_inlineMix_btns(
            btns={
                "✈️ Telegram": "https://t.me/mtuci_official",
                "✅ Вконтакте": "https://vk.com/mtuci",
                "🌐 Официальный сайт": "https://mtuci.ru",
            }
        ),
    )

# #Высылает ID фото ответным сообщением.
# @user_private_router.message()
# async def photo_info (message:types.Message):
#     image=message.photo[-1].file_id
#     await message.answer(f"id {image}")
