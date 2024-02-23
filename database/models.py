from sqlalchemy import DateTime, Integer, func, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Questions(Base):
    __tablename__ = 'messages_from_users_new2'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer(), nullable=False)

class Keywords_list(Base):
    __tablename__ = 'keywords_list'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(Text)

class Ready_Answers(Base):
    __tablename__ = 'ready_answers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    answer: Mapped[str] = mapped_column(Text)
    
class Keyword_Answers(Base):
    __tablename__ = 'keyword_answers_idkeys'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    keyword_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    answer_id: Mapped[int] = mapped_column(Integer(), nullable=False)