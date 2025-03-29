import asyncio
# import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database.env import DATABASE_URL
from repositories.teacher import TeacherRepository


# logging.basicConfig(level=logging.WARNING)
# logging.getLogger('sqlalchemy').setLevel(logging.WARNING)


async def main():
    # Создание асинхронного движка и сессии
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        repo = TeacherRepository(session)

        # Пример использования репозитория
        await repo.add_teacher("123456791", "Кто-то ктотович 111")
        teacher = await repo.get_teacher_by_telegram_id("123456790")
        print(f"Retrieved Teacher: {teacher.name}")

        # await repo.update_teacher("123456789", "Jane Doe")
        # updated_teacher = await repo.get_teacher_by_telegram_id("123456789")
        # print(f"Updated Teacher: {updated_teacher.name}")

        # await repo.delete_teacher("123456787")
        # deleted_teacher = await repo.get_teacher_by_telegram_id("123456789")
        # print(f"Deleted Teacher: {deleted_teacher}")

asyncio.run(main())
