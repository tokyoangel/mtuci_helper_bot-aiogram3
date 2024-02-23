from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Questions, Keywords_list, Ready_Answers, Keyword_Answers


async def orm_add_question(session: AsyncSession, data: dict):
    obj = Questions(
        message_id=data["message_id"],
        chat_id=data["chat_id"],
    )
    session.add(obj)
    await session.commit()


async def orm_get_questions(session: AsyncSession):
    query = select(Questions)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_question(session: AsyncSession, message_id: int):
    query = select(Questions).where(Questions.id == message_id)
    result = await session.execute(query)
    return result.scalar()

#№№----- Для добавления в БД keywords и answers

#Добавление ключевых слов

async def orm_add_keywords(session: AsyncSession, data: dict):
    obj = Keywords_list(word=data["word"])
    session.add(obj)
    await session.commit()
#Получение ключевых слов
async def orm_get_keywords(session: AsyncSession):
    query = select(Keywords_list)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_delete_keywords(session: AsyncSession):
    query = delete(Keywords_list)
    await session.execute(query)
    await session.commit()



#Добавление ответов
async def orm_add_answers(session: AsyncSession, data: dict):
    obj = Ready_Answers(answer=data["answer"])
    session.add(obj)
    await session.commit()
#Получене ответов
async def orm_get_answers(session: AsyncSession):
    query = select(Ready_Answers)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_delete_answers(session: AsyncSession):
    query = delete(Ready_Answers)
    await session.execute(query)
    await session.commit()
    
async def orm_get_answer1(session: AsyncSession, answer_id: int):
    query = select(Ready_Answers).where(Ready_Answers.id == answer_id)
    result = await session.execute(query)
    return result.scalar()


#Добавление ответов
#Добавление в БД пар [keyword_id,answer_id]
async def orm_add_keyword_answer(session: AsyncSession, data: dict):
    obj = Keyword_Answers(
        keyword_id=data["keyword_id"],
        answer_id=data["answer_id"],
    )
    session.add(obj)
    await session.commit()

async def orm_get_keywords_answers(session: AsyncSession):
    query = select(Keyword_Answers)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_keyword_answer(session: AsyncSession,keyword_id: int):
    query = select(Keyword_Answers).select_from(Ready_Answers).where(Ready_Answers.id == keyword_id)
    result = await session.execute(query)
    return result.scalars().all()

# async def orm_get_keyword_answer(session: AsyncSession, keyword_id: int):
#     query = select(Ready_Answers).where(Ready_Answers.id == keyword_id)
#     result = await session.execute(query)
#     # Преобразование каждой записи в словарь
#     keyword_answers = [record._asdict() for record in result.scalars().all()]
#     return keyword_answers

async def orm_delete_keyword_answer(session: AsyncSession):
    query = delete(Keyword_Answers)
    await session.execute(query)
    await session.commit()
