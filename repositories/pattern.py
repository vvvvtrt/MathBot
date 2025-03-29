from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from database.models import Patterns


class PatternRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_pattern(self, teacher_id: int, pattern_name: str,
                          generated_images: str = None,
                          answers_to_tasks: str = None) -> Patterns | None:
        new_pattern = Patterns(teacher_id=teacher_id,
                               pattern_name=pattern_name,
                               generated_images=generated_images,
                               answers_to_tasks=answers_to_tasks)
        try:
            self.session.add(new_pattern)
            await self.session.commit()
            return new_pattern
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error adding pattern: {e}")
            return None

    async def get_pattern_by_id(self, pattern_id: int) -> Patterns | None:
        try:
            result = await self.session.execute(select(Patterns).filter_by(
                pattern_id=pattern_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error getting pattern: {e}")
            return None

    async def get_patterns_by_teacher_id(
            self, teacher_id: int) -> list[Patterns] | None:
        try:
            result = await self.session.execute(select(Patterns).filter_by(
                teacher_id=teacher_id))
            return result.scalars().all()  # Возвращаем паттерны для учителя
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error getting patterns by teacher_id: {e}")
            return None

    async def update_pattern(self, pattern_id: int, pattern_name: str,
                             generated_images: str = None,
                             answers_to_tasks: str = None) -> Patterns | None:
        try:
            pattern = await self.get_pattern_by_id(pattern_id)
            if pattern:
                pattern.pattern_name = pattern_name
                pattern.generated_images = generated_images
                pattern.answers_to_tasks = answers_to_tasks
                await self.session.commit()
                return pattern
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error updating pattern: {e}")
        return None

    async def delete_pattern(self, pattern_id: int) -> Patterns | None:
        try:
            pattern = await self.get_pattern_by_id(pattern_id)
            if pattern:
                await self.session.delete(pattern)
                await self.session.commit()
                return pattern
        except SQLAlchemyError as e:
            await self.session.rollback()  # Откат транзакции
            print(f"Error deleting pattern: {e}")
            return None
