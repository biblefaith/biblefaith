from loguru import logger
from peewee import Model, SqliteDatabase, DateTimeField, CharField, TextField, ForeignKeyField, BooleanField, IntegerField, IntegrityError, PeeweeException
from datetime import datetime, timezone

# Настройка логирования с Loguru
logger.add("debug.log", rotation="10 MB")  # Логи будут записываться в файл debug.log, который будет перекатываться после достижения 10 МБ

# Создаем соединение с базой данных SQLite
db = SqliteDatabase('bot.db')

class BaseModel(Model):
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # Use UTC time for all records

    class Meta:
        database = db
        legacy_table_names = False

class Text(BaseModel):
    content = TextField()
    type = CharField(max_length=20)

class Question(BaseModel):
    text = TextField()
    text_related = ForeignKeyField(Text, backref='questions', on_delete='SET NULL')  # Change on_delete behavior
    type = CharField(max_length=20)

class Student(BaseModel):
    telegram_id = IntegerField(unique=True)
    telegram_full_name = CharField(max_length=100, null=True)
    telegram_username = CharField(max_length=100, null=True)
    status = BooleanField(default=True)
    text_type = CharField(max_length=20, null=True)
    question_type = CharField(max_length=20, null=True)

    @classmethod
    def create_or_update(cls, telegram_id, **kwargs):
        with cls._meta.database.atomic():  # Start transaction
            try:
                student, created = cls.get_or_create(telegram_id=telegram_id)
                if created:
                    logger.info(f"Student {telegram_id} created successfully.")
                for key, value in kwargs.items():
                    if getattr(student, key, None) != value:
                        setattr(student, key, value)
                student.save()
                logger.info(f"Student {telegram_id} updated successfully.")
                return student, created
            except (IntegrityError, PeeweeException) as e:
                logger.error(f"Error updating or creating student: {e}")
                raise e  # Optionally re-raise the exception for further handling outside

class Answer(BaseModel):
    student = ForeignKeyField(Student, backref='answers')
    question = ForeignKeyField(Question, backref='answers', on_delete='CASCADE')
    answer = TextField()

class Teacher(BaseModel):
    name = CharField(max_length=100)

class ReadingProgress(BaseModel):
    student = ForeignKeyField(Student, backref='reading_progress')
    text = ForeignKeyField(Text, backref='reading_progress', on_delete='CASCADE')
    current_question = ForeignKeyField(Question, related_name='reading_progress', on_delete='SET NULL', null=True)
    position = IntegerField(default=0)

class ReadingPlans(Model):
    day_number = IntegerField()
    start_text_number = IntegerField()
    end_text_number = IntegerField()
    plan_name = CharField(max_length=100)
    class Meta:
        database = db
        legacy_table_names = False


class Verses(Model):
    book_number = IntegerField()
    chapter = IntegerField()
    verse = IntegerField()
    content_value = TextField()
    text_number = IntegerField()
    content_variety = CharField(max_length=20)
    class Meta:
        database = db
        legacy_table_names = False


if __name__ == "__main__":
    db.connect()
    db.create_tables([Text, Question, Student, Answer, Teacher, ReadingProgress, ReadingPlans, Verses], safe=True)
