import os
from aiogram import F, Router, types, Bot

from aiogram.filters import Command, StateFilter, or_f
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_question, orm_get_questions

bot = Bot(token=os.getenv("TOKEN"))

# bot=
send_to_group_router = Router()
send_to_group_router.message.filter(ChatTypeFilter(["private"]))
GROUP_CHAT_ID = os.getenv("TELEGRAM_SUPPORT_CHAT_ID")


class AddQuestion(StatesGroup):
    message_id = State()
    chat_id = State()

    message_pairs = None


@send_to_group_router.message(StateFilter(None), or_f(F.text == "Обратная связь", Command("writeme")))
async def add_question(message: types.Message, state: FSMContext):
    await message.answer("Введите Ваш вопрос")
    await state.set_state(AddQuestion.message_id)


@send_to_group_router.message(AddQuestion.message_id)
async def send_txt_to_group(
    message: types.Message, state: FSMContext, session: AsyncSession
):

    if len(message.text) >= 1000:
        await message.answer(
            "Сообщение не должно превышать 1000 символов. \n Введите заново"
        )
        return
    # Отправляем сообщение в группу и сохраняем его ID
    
    
    
    sent_message = await bot.send_message(
        GROUP_CHAT_ID, f"Новое обращение.\nСообщение от  {message.from_user.first_name}:\n{message.text}"
    )
    # Сохраняем соответствие между ID сообщения пользователя и сообщением в группе

    await state.update_data(message_id=sent_message.message_id)
    await state.update_data(chat_id=message.chat.id)
    data = await state.get_data()

    await orm_add_question(session, data)

    await state.clear()
    AddQuestion.message_pairs = None
    await message.answer("Ваше сообщение отправлено. Ожидайте.")


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
