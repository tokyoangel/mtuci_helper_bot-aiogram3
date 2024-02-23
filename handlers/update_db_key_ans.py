import os
import re
import aiofiles
from aiogram import Router, types, Bot
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter

from sqlalchemy.ext.asyncio import AsyncSession

from kbds.reply import get_keyboard

from database.orm_query import (
    orm_add_keywords,
    orm_get_keywords,
    orm_delete_keywords,
    orm_add_answers,
    orm_get_answers,
    orm_delete_answers,
    orm_add_keyword_answer,
    # orm_get_keyword_answer,
    orm_delete_keyword_answer,
)

bot = Bot(token=os.getenv("TOKEN"))

file_keywords_path = "data_for_db\keyword_list.txt"
file_answers_path = "data_for_db\kanswer_list.txt"


# bot=
update_db_key_ans_router = Router()
# update_db_key_ans_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


# Выполнять после определённой команды /update_db
@update_db_key_ans_router.message(Command("update_db"))
async def start_update_db(message: types.Message, session: AsyncSession):
    await message.answer(
        "Обновление началось.", reply_markup=types.ReplyKeyboardRemove()
    )
    await input_keywords(session)
    await message.answer("База ключевых слов обновлена.\n")
    await input_answers(session)
    await message.answer("База ответов обновлена.\n")
    await input_keyword_answer(session)
    await message.answer("База пар ключей обновлена.\n")
    await message.answer(
        "Обновление завершено.",
        reply_markup=get_keyboard(
            "О МТУСИ/Контакты",
            "Как добраться",
            "Приёмная комиссия",
            "Общежитие",
            "Обратная связь",
            placeholder="Что Вас интересует?",
            sizes=(2, 2),
        ),
    )


async def input_keywords(session: AsyncSession):
    # Открытие файла и чтение строк
    await orm_delete_keywords(session)
    with open(file_keywords_path, "r", encoding="utf-8") as file:
        for line in file:
            #       Удаление пробельных символов с обеих сторон строки
            keyword = line.strip()
            # Добавление ключевого слова в базу данных
            if keyword:  # Проверка, что строка не пустая
                await orm_add_keywords(session, {"word": keyword})


# Теперь переменная words содержит список слов из файла
async def input_answers(session: AsyncSession):
    await orm_delete_answers(session)
    with open(file_answers_path, mode="r", encoding="utf-8") as file:
        file_content = file.read()
        # Поиск всех подстрок, заключенных в кавычки
        answers = re.findall(r'"(.*?)"', file_content, re.DOTALL)
        for answer in answers:
            data2 = {"answer": answer}
            await orm_add_answers(session, data2)



async def input_keyword_answer(session: AsyncSession):
    await orm_delete_keyword_answer(session)
    for keyword_ch in await orm_get_keywords(session):
        for answer_ch in await orm_get_answers(session):
            if keyword_ch.word.lower() in answer_ch.answer.lower():
                data3 = {
                    "keyword_id": f"{keyword_ch.id}",
                    "answer_id": f"{answer_ch.id}",
                }
                await orm_add_keyword_answer(session, data3)
