import os
from aiogram import F, Router, types, Bot

from aiogram.filters import Command, StateFilter, or_f
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from kbds.reply import get_keyboard
from kbds.inline import get_callback_btns
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from collections import defaultdict

from handlers.yandexgpt import generate_answer
from database.engine import session_maker
from database.orm_query import (
    orm_add_question,
    orm_get_answer1,
    orm_get_keywords_answers,
    orm_get_questions,
)
from database.orm_query import orm_get_keywords, orm_get_keyword_answer, orm_get_answers

bot = Bot(token=os.getenv("TOKEN"))

# bot=
send_to_group_router = Router()
send_to_group_router.message.filter(ChatTypeFilter(["private"]))
GROUP_CHAT_ID = os.getenv("TELEGRAM_SUPPORT_CHAT_ID")

GLobalMessage = None


class AddQuestion(StatesGroup):
    bd_yagpt = State()
    spec_chat_id = State()




@send_to_group_router.message(
    StateFilter(None), or_f(F.text == "Обратная связь", Command("writeme"))
)
async def add_question(message: types.Message, state: FSMContext):
    await message.answer(
        "Задайте свой вопрос.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(AddQuestion.bd_yagpt)


@send_to_group_router.message(AddQuestion.bd_yagpt)
async def send_to_bd_yagpt(
    message: types.Message, state: FSMContext, session: AsyncSession
):
    if len(message.text) >= 1000:
        await message.answer(
            "Сообщение не должно превышать 1000 символов. \n Введите заново"
        )
        return
    
    #await bot.send_message(1772168991, text=f"--- Вопрос пользователя в YandexGPT---\n{message.text}")
    answer_from_bd = await find_answers_for_user_message(session, message.text)
    await message.answer(f"{answer_from_bd}")
    #await bot.send_message(1772168991, text=f"--- Ответ YandexGPT---\n{answer_from_bd}")

    # await state.clear()
    await message.answer(
        "Если ответ Вам помог, нажмите Выход, в остальных случаях Связаться со специалистом",
        reply_markup=get_callback_btns(
            btns={
                "Выход": "stop_",
                "Связаться со специалистом": "special_",
            }
        ),
    )


async def find_answers_for_user_message(session: AsyncSession, user_message):
    # 1. Асинхронное извлечение всех ключевых слов из базы данных
    keywords_query = await orm_get_keywords(session)

    # 2. Находим ключевые слова, которые присутствуют в сообщении пользователя
    found_keyword_ids = None# [keyword.id for keyword in keywords_query if keyword.word in user_message] 

    # print("found_keyword_ids {found_keyword_ids}")
    answer = await generate_answer(user_message)
    if not found_keyword_ids:
        return answer
    answers_query_id = await orm_get_keywords_answers(session)
    print("answers_query_id = {answers_query_id}")
    # 3. Находим все id ответов, связанные с найденными ключевыми словами
    for each_key in found_keyword_ids:
            answers_query_id = await orm_get_keyword_answer(session, each_key)
            final_answers = await orm_get_answer1(session,answers_query_id)

    return answer  # final_answers


@send_to_group_router.callback_query(F.data.startswith("stop_"))
async def stop_cycle(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    # await bot.answer_callback(callback.id)
    await callback.message.answer(
        "Вы вышли из чата.",
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


@send_to_group_router.callback_query(F.data.startswith("special_"))
async def change_fsm_for_group(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Переход в чат с специалистом.\nВведите Ваш вопрос для специалиста."
    )
    await state.set_state(AddQuestion.spec_chat_id)


@send_to_group_router.message(AddQuestion.spec_chat_id)
async def send_to_group_chat(
    message: types.Message, state: FSMContext, session: AsyncSession
):

    if len(message.text) >= 1000:
        await message.answer(
            "Сообщение не должно превышать 1000 символов. \n Введите заново"
        )
        return
    
    # await message.answer("Введите Ваш вопрос для специалиста.")
    sent_message = await bot.send_message(
        GROUP_CHAT_ID,
        f"Новое обращение.\nСообщение от  {message.from_user.first_name}:\n{message.text}",
    )
    # Сохраняем соответствие между ID сообщения пользователя и сообщением в группе
    await state.update_data(message_id=sent_message.message_id)
    await state.update_data(chat_id=message.chat.id)
    data = await state.get_data()

    await orm_add_question(session, data)

    # await state.clear()
    AddQuestion.message_pairs = None
    await message.answer(
        "Ожидайте ответ.",
        reply_markup=get_callback_btns(
            btns={
                "Выход": "stop_",
            }
        ),
    )
    await state.set_state(AddQuestion.spec_chat_id)


group_adm_router = Router()
group_adm_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


# bot
@group_adm_router.message()
async def send_to_user(message: types.Message, session: AsyncSession):
    if message.reply_to_message:
        for questions in await orm_get_questions(session):
            if questions.message_id == message.reply_to_message.message_id:
                await bot.send_message(
                    questions.chat_id, f"Ответ на Ваше обращение: {message.text}"
                )
