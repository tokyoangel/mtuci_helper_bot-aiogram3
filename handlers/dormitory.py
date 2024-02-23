import os
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from filters.chat_types import ChatTypeFilter

from kbds.inline import get_inlineMix_btns, get_callback_btns

from texts_message.dormitory_txt import (
    dormitory_txt_start,
    dormitory_txt1,
    dormitory_txt3,
    dormitory_txt4,
    dormitory_txt_info,
)

dormitory_router = Router()
dormitory_router.message.filter(ChatTypeFilter(["private"]))


@dormitory_router.message(F.text.lower() == "общежитие")
@dormitory_router.message(Command("dormitory"))
async def where_def(message: types.Message | CallbackQuery):

    await message.answer(
        dormitory_txt_start,
        reply_markup=get_callback_btns(
            btns={
                "Информация": "dormitory_info",
                "Общежитие 1": "dormitory_1",
                "Общежитие 3": "dormitory_3",
                "Общежитие 4": "dormitory_4",
            }
        ),
    )


@dormitory_router.callback_query(F.data.startswith("dormitory"))
async def chouse_camp(callback: types.CallbackQuery):
    campus = callback.data
    if campus == "dormitory_info":
        await callback.message.answer(dormitory_txt_info)
    elif campus == "dormitory_1":
        await callback.message.answer_photo(photo=os.getenv("dormitory_1"))
        await callback.message.answer(
            dormitory_txt1,
            reply_markup=get_inlineMix_btns(
                btns={
                    "Google Карты": "https://maps.app.goo.gl/zmdnZ5YZb258WXvk8",
                    "Яндекс карты": "https://yandex.ru/maps/-/CDBziJ4i",
                }
            ),
        )
    elif campus == "dormitory_3":
        await callback.message.answer_photo(photo=os.getenv("dormitory_3"))
        await callback.message.answer(
            dormitory_txt3,
            reply_markup=get_inlineMix_btns(
                btns={
                    "Google Карты": "https://maps.app.goo.gl/SXRFsM1UKfDVMnVG9",
                    "Яндекс карты": "https://yandex.ru/maps/-/CDBzVB7w",
                }
            ),
        )
    else:
        await callback.message.answer_photo(photo=os.getenv("dormitory_4"))
        await callback.message.answer(
            dormitory_txt4,
            reply_markup=get_inlineMix_btns(
                btns={
                    "Google Карты": "https://maps.app.goo.gl/ZoNhFgD5AeLsaZgP6",
                    "Яндекс карты": "https://yandex.ru/maps/-/CDBzVF3y",
                }
            ),
        )
