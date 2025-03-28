from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from database.models import Students


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_student(self, teacher_id: int,
                          telegram_id: str, name: str,
                          pattern_id: int = None) -> Students | None:
        new_student = Students(
            teacher_id=teacher_id, telegram_id=telegram_id,
            name=name, pattern_id=pattern_id)
        try:
            self.session.add(new_student)
            await self.session.commit()
            return new_student
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error adding student: {e}")
            return None

    async def get_student_by_telegram_id(self,
                                         telegram_id: str) -> Students | None:
        try:
            result = await self.session.execute(select(Students).filter_by(
                telegram_id=telegram_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error getting student: {e}")
            return None

    async def update_student(self, telegram_id: str, name: str,
                             pattern_id: int = None) -> Students | None:
        try:
            student = await self.get_student_by_telegram_id(telegram_id)
            if student:
                student.name = name
                student.pattern_id = pattern_id
                await self.session.commit()
                return student
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error updating student: {e}")
        return None

    async def delete_student(self, telegram_id: str) -> Students | None:
        try:
            student = await self.get_student_by_telegram_id(telegram_id)
            if student:
                await self.session.delete(student)
                await self.session.commit()
                return student
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error deleting student: {e}")
            return None
