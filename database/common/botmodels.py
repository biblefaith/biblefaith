from peewee import Model, SqliteDatabase, DateTimeField, CharField, TextField, ForeignKeyField, BooleanField, IntegerField
from datetime import datetime

# Создаем соединение с базой данных SQLite
db = SqliteDatabase('bot_database.db')

# Определяем базовый класс модели данных
class BaseModel(Model):
    # Поле для даты создания с дефолтным текущим значением времени
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        legacy_table_names = False

# Определяем модель для текстов для чтения
class Text(BaseModel):
    content = TextField()
    type = CharField(max_length=20)  # 'устаревший перевод' или 'современный перевод'

# Определяем модель для вопросов к текстам
class Question(BaseModel):
    text = TextField()
    text_related = ForeignKeyField(Text, backref='questions')
    type = CharField(max_length=20)  # 'для новичков' или 'для продвинутых'

# Определяем модель для студентов
class Student(BaseModel):
    telegram_id = IntegerField(unique=True)  # Идентификатор Telegram студента (числовой формат)
    status = BooleanField(default=True)  # True - активный студент, False - исключенный студент
    text_type = CharField(max_length=20, null=True)  # Тип текста, выбранный студентом
    question_type = CharField(max_length=20, null=True)  # Тип вопросов, выбранный студентом
    @classmethod
    def create_or_update(cls, telegram_id, **kwargs):
        # Пытаемся найти студента по telegram_id
        student = cls.get_or_none(telegram_id=telegram_id)
        if student:
            # Если студент найден, обновляем его атрибуты
            for key, value in kwargs.items():
                setattr(student, key, value)
            student.save()  # Сохраняем изменения
        else:
            # Если студент не найден, создаем нового
            cls.create(telegram_id=telegram_id, **kwargs)

    @classmethod
    def get_student(cls, telegram_id):
        # Получаем студента по telegram_id
        return cls.get_or_none(telegram_id=telegram_id)

# Определяем модель для ответов студентов на вопросы
class Answer(BaseModel):
    student = ForeignKeyField(Student, backref='answers')
    question = ForeignKeyField(Question, backref='answers')
    answer = TextField()

# Определяем модель для преподавателей
class Teacher(BaseModel):
    name = CharField(max_length=100)

# Определяем модель для отслеживания прогресса чтения студентов
class ReadingProgress(BaseModel):
    student = ForeignKeyField(Student, backref='reading_progress')
    text = ForeignKeyField(Text, backref='reading_progress')
    current_question = ForeignKeyField(Question, backref='reading_progress')
    position = IntegerField(default=0)  # текущая позиция чтения в тексте (например, номер страницы или номер вопроса)

if __name__ == "__main__":
    # Создаем таблицы в базе данных
    db.connect()
    db.create_tables([Text, Question, Student, Answer, Teacher, ReadingProgress])
