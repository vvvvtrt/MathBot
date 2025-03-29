from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from database.models import Teachers


class TeacherRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_teacher(self, telegram_id: str,
                          name: str) -> Teachers | None:
        new_teacher = Teachers(telegram_id=telegram_id, name=name)
        try:
            self.session.add(new_teacher)
            await self.session.commit()
            return new_teacher
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error adding teacher: {e}")
            return None

    async def get_teacher_by_telegram_id(self,
                                         telegram_id: str) -> Teachers | None:
        try:
            result = await self.session.execute(select(Teachers).filter_by(
                telegram_id=telegram_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error getting teacher: {e}")
            return None

    async def update_teacher(self, telegram_id: str,
                             name: str) -> Teachers | None:
        try:
            teacher = await self.get_teacher_by_telegram_id(telegram_id)
            if teacher:
                teacher.name = name
                await self.session.commit()
                return teacher
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error updating teacher: {e}")
        return None

    async def delete_teacher(self, telegram_id: str) -> Teachers | None:
        try:
            teacher = await self.get_teacher_by_telegram_id(telegram_id)
            if teacher:
                await self.session.delete(teacher)
                await self.session.commit()
                return teacher
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error deleting teacher: {e}")
            return None
