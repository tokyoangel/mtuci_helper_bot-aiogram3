from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Questions


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


