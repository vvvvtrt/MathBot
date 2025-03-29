from repositories.teacher import TeacherRepository
from repositories.pattern import PatternRepository


class TeacherService:
    def __init__(self, teacher_repository: TeacherRepository, pattern_repository: PatternRepository):
        self.teacher_repository = teacher_repository
        self.pattern_repository = pattern_repository

    async def create_teacher(self, telegram_id: str, name: str):
        teacher = await self.teacher_repository.get_teacher_by_telegram_id(telegram_id)
        if teacher is not None:
            return teacher
        else:
            return await self.teacher_repository.add_teacher(telegram_id=telegram_id, name=name)

    async def create_pattern(self, teacher_telegram_id: str, pattern_name: str,
                             generated_images: str = None, answers_to_tasks: str = None):
        teacher = await self.teacher_repository.get_teacher_by_telegram_id(teacher_telegram_id)
        if teacher:
            return await self.pattern_repository.add_pattern(
                teacher_id=teacher.teacher_id,
                pattern_name=pattern_name,
                generated_images=generated_images,
                answers_to_tasks=answers_to_tasks
            )
        return None

    async def get_patterns_by_teacher_telegram_id(self, telegram_id: str):
        teacher = await self.teacher_repository.get_teacher_by_telegram_id(telegram_id)
        if teacher:
            return await self.pattern_repository.get_patterns_by_teacher_id(teacher.teacher_id)
        return None

    async def get_pattern_by_teacher_telegram_id_and_name(self, telegram_id: str, pattern_name: str):
        teacher = await self.teacher_repository.get_teacher_by_telegram_id(telegram_id)
        if teacher:
            patterns = await self.pattern_repository.get_patterns_by_teacher_id(teacher.teacher_id)
            for pattern in patterns:
                if pattern.pattern_name == pattern_name:
                    return pattern
        return None

    async def update_pattern(self, telegram_id: str, pattern_name: str, new_pattern_name: str = None,
                             generated_images: str = None, answers_to_tasks: str = None):
        teacher = await self.teacher_repository.get_teacher_by_telegram_id(telegram_id)
        if teacher:
            patterns = await self.pattern_repository.get_patterns_by_teacher_id(teacher.teacher_id)
            for pattern in patterns:
                if pattern.pattern_name == pattern_name:
                    return await self.pattern_repository.update_pattern(
                        pattern_id=pattern.pattern_id,
                        pattern_name=new_pattern_name or pattern.pattern_name,
                        generated_images=generated_images or pattern.generated_images,
                        answers_to_tasks=answers_to_tasks or pattern.answers_to_tasks
                    )
        return None
