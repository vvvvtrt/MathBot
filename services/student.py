from repositories.teacher import TeacherRepository
from repositories.pattern import PatternRepository
from repositories.student import StudentRepository


class StudentService:
    def __init__(self, student_repository: StudentRepository, pattern_repository: PatternRepository, teacher_repository: TeacherRepository):
        self.student_repository = student_repository
        self.pattern_repository = pattern_repository
        self.teacher_repository = teacher_repository

    async def create_student(self, teacher_id: int, telegram_id: str, name: str, pattern_id: int = None):
        return await self.student_repository.add_student(teacher_id=teacher_id, telegram_id=telegram_id, name=name, pattern_id=pattern_id)

    async def get_patterns_by_student_telegram_id(self, telegram_id: str):
        # student_teacher_id = await self.student_repository.get_student_by_telegram_id(telegram_id).teacher_id
        patterns_ids = await self.student_repository.get_patterns_id_by_telegram_id(telegram_id)
        patterns = []
        for pattern_id in patterns_ids:
            patterns += [await self.pattern_repository.get_pattern_by_id(pattern_id)]
        return patterns

    async def assign_pattern_to_student(self, student_telegram_id: str, teacher_telegram_id: str, pattern_name: str):
        student = await self.student_repository.get_student_by_telegram_id(student_telegram_id)
        if student:
            patterns = await self.pattern_repository.get_patterns_by_teacher_id(student.teacher_id)
            for pattern in patterns:
                if pattern.pattern_name == pattern_name:
                    await self.student_repository.update_student(telegram_id=student_telegram_id, name=student.name, pattern_id=pattern.pattern_id)
                    return student
        return None

    async def update_student_pattern(self, telegram_id: str, new_pattern_id: int):
        student = await self.student_repository.get_student_by_telegram_id(telegram_id)
        if student:
            student.pattern_id = new_pattern_id
            return await self.student_repository.update_student(telegram_id=telegram_id, name=student.name, pattern_id=new_pattern_id)
        return None
