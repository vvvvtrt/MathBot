import asyncio

from repositories.teacher import TeacherRepository
from repositories.pattern import PatternRepository
from repositories.student import StudentRepository
from services.teacher import TeacherService
from services.student import StudentService
from database.session import get_async_session


async def test_teacher_service():
    async with get_async_session() as session:
        teacher_repository = TeacherRepository(session)
        pattern_repository = PatternRepository(session)
        teacher_service = TeacherService(
            teacher_repository, pattern_repository)

        # 1. Создание учителя
        new_teacher = await teacher_service.create_teacher(telegram_id="123456790", name="Иван Иванов")
        if new_teacher is not None:
            print(f"[TEST] Созданный учитель: {new_teacher.name}")

        # 2. Создание паттернов для учителя
        new_pattern_1 = await teacher_service.create_pattern(
            teacher_telegram_id="123456790",
            pattern_name="Шаблон 1",
            generated_images="изображения_1",
            answers_to_tasks="ответы_1"
        )
        new_pattern_2 = await teacher_service.create_pattern(
            teacher_telegram_id="123456790",
            pattern_name="Шаблон 2",
            generated_images="изображения_2",
            answers_to_tasks="ответы_2"
        )
        print(
            f"[TEST] Созданные паттерны: {new_pattern_1.pattern_name}, {new_pattern_2.pattern_name}")

        # 3. Получение всех шаблонов по telegram_id учителя
        patterns = await teacher_service.get_patterns_by_teacher_telegram_id("123456790")
        print("[TEST] Шаблоны учителя:", [
              pattern.pattern_name for pattern in patterns])

        # 4. Получение конкретного шаблона по telegram_id учителя и имени шаблона
        specific_pattern = await teacher_service.get_pattern_by_teacher_telegram_id_and_name("123456790", "Шаблон 1")
        print(f"[TEST] Найденный шаблон: {specific_pattern.pattern_name}")

        # 5. Обновление шаблона
        updated_pattern = await teacher_service.update_pattern(
            telegram_id="123456790",
            pattern_name="Шаблон 1",
            new_pattern_name="Обновленный Шаблон 1",
            generated_images="новые_изображения 1",
            answers_to_tasks="новые_ответы 1"
        )
        print(f"[TEST] Обновленный шаблон: {updated_pattern.pattern_name}")


async def test_student_service():
    async with get_async_session() as session:
        student_repository = StudentRepository(session)
        pattern_repository = PatternRepository(session)
        student_service = StudentService(
            student_repository, pattern_repository)

        # 1. Создание студента
        new_student = await student_service.create_student(teacher_id=1, telegram_id="987654321", name="Петр Петров")
        print(f"Созданный студент: {new_student}")

        # 2. Получение всех паттернов по telegram_id студента
        patterns = await student_service.get_patterns_by_student_telegram_id("987654321")
        print(f"Паттерны студента: {patterns}")

        # 3. Запись паттерна студенту
        assigned_pattern = await student_service.assign_pattern_to_student(
            student_telegram_id="987654321",
            teacher_telegram_id="123456789",
            pattern_name="Шаблон 1"
        )
        print(f"Записанный паттерн студенту: {assigned_pattern}")

        # 4. Изменение задания (паттерна) для студента
        updated_student = await student_service.update_student_pattern(
            telegram_id="987654321",
            new_pattern_id=2  # Предполагается, что 2 - это ID нового паттерна
        )
        print(f"Обновленный студент: {updated_student}")

asyncio.run(test_teacher_service())
# asyncio.run(test_student_service())
