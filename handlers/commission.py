import os
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from filters.chat_types import ChatTypeFilter

from kbds.inline import get_inlineMix_btns

from texts_message.commission_txt import (
    commission_txt1,
    commission_txt2,
    commission_txt3,
    commission_txt4,
)


commission_router = Router()
commission_router.message.filter(ChatTypeFilter(["private"]))


@commission_router.message(F.text.lower() == "приёмная комиссия")
@commission_router.message(Command("comission"))
async def commission(message: types.Message | CallbackQuery):
    await message.answer(
        commission_txt1,
        reply_markup=get_inlineMix_btns(
            btns={
                "ГосУслуги": "commission_gosuslugi",
                "Официальный сайт": "commission_official",
                "Личное присутствие": "commission_you",
            }
        ),
    )


@commission_router.callback_query(F.data.startswith("commission_"))
async def chouse_camp(callback: types.CallbackQuery):
    commission_check = callback.data
    if commission_check == "commission_gosuslugi":
        await callback.message.answer(
            commission_txt2,
            reply_markup=get_inlineMix_btns(
                btns={"ГосУслуги": "https://www.gosuslugi.ru/10077/1"}
            ),
        )
    elif commission_check == "commission_official":
        await callback.message.answer(
            commission_txt3,
            reply_markup=get_inlineMix_btns(
                btns={
                    "Личный кабинет": "https://lk.abitur.mtuci.ru/user/sign-in/login",
                    "Telegram": "https://t.me/mtuci_abitur",
                }
            ),
        )
        await callback.message.answer(
            "Если сложно определиться со специальностью, ведите Ваши баллы ЕГЭ, а наш помощник даст Вам рекомендации по выбору конкурсных направлений подготовки на бюджетные места",
            reply_markup=get_inlineMix_btns(
                btns={"Помощник": "https://abitur.mtuci.ru/abitur_helper/"}
            ),
        )
    else:
        await callback.message.answer(commission_txt4)
        await callback.message.answer_photo(photo=os.getenv("main_camp_mtuci_photo"))
        await callback.message.answer(
            " На фотографии главный вход.\nАдрес: Авиамоторная улица, 8с\nНе забудьте взять с собой документы!",
            reply_markup=get_inlineMix_btns(
                btns={
                    "Google Карты": "https://maps.app.goo.gl/z8Z8caAZQkdMPZhc8",
                    "Яндекс карты": "https://yandex.ru/maps/-/CDBreOJS",
                }
            ),
        )
