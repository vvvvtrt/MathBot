from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Teachers(Base):
    __tablename__ = 'teachers'

    teacher_id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    name = Column(String)

    # Связь с Patterns
    patterns = relationship('Patterns', back_populates='teacher')
    # Связь со Students
    students = relationship('Students', back_populates='teacher')


class Patterns(Base):
    __tablename__ = 'patterns'

    pattern_id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey(
        'teachers.teacher_id'), nullable=False)
    pattern_name = Column(String, nullable=False)
    generated_images = Column(String)
    answers_to_tasks = Column(String)

    # Связь с Teachers
    teacher = relationship('Teachers', back_populates='patterns')


class Students(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey(
        'teachers.teacher_id'), nullable=False)
    telegram_id = Column(String, unique=True, nullable=False)
    name = Column(String)
    pattern_id = Column(Integer, ForeignKey('patterns.pattern_id'))

    # Связь с Teachers
    teacher = relationship('Teachers', back_populates='students')
    # Связь с Patterns
    pattern = relationship('Patterns')
