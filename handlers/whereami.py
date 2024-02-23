import os
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery
from filters.chat_types import ChatTypeFilter

from kbds.inline import get_inlineMix_btns, get_callback_btns

from texts_message import whereami_txt


whereami_router = Router()
whereami_router.message.filter(ChatTypeFilter(["private"]))

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@whereami_router.message(F.text.lower() == "как добраться")
@whereami_router.message(Command("where"))
async def where_def(message: types.Message | CallbackQuery):

    await message.answer(
        whereami_txt.whereami,
        reply_markup=get_callback_btns(
            btns={"Главный кампус": "camp_main", "Второй кампус": "camp_second"}
        ),
    )


@whereami_router.callback_query(F.data.startswith("camp_"))
async def chouse_camp(callback: types.CallbackQuery):
    campus = callback.data
    if campus == "camp_main":
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
    else:
        await callback.message.answer_photo(photo=os.getenv("second_camp_mtuci"))
        await callback.message.answer(
            " На фотографии главный вход.\nАдрес: ул. Народного Ополчения, 32\nНе забудьте взять с собой документы!",
            reply_markup=get_inlineMix_btns(
                btns={
                    "Google Карты": "https://maps.app.goo.gl/zTs8dDF2GAft18SU6",
                    "Яндекс карты": "https://yandex.ru/maps/-/CDBriA-F",
                }
            ),
        )
