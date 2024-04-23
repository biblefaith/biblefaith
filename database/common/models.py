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

class Text(Model):
    day_number = IntegerField()
    content = TextField()
    type = CharField(max_length=20)
    class Meta:
        database = db

class Question(Model):
    day_number = IntegerField()
    ordering_number = IntegerField()
    content = TextField()
    type = CharField(max_length=20)
    class Meta:
        database = db

class Student(BaseModel):
    telegram_id = IntegerField(unique=True)
    telegram_full_name = CharField(max_length=100, null=True)
    telegram_username = CharField(max_length=100, null=True)
    status = BooleanField(default=True)
    text_type = CharField(max_length=20, null=True)
    question_type = CharField(max_length=20, null=True)

    def save_progress(self, text, question):
        with db.atomic():
            try:
                progress, created = Progress.get_or_create(student=self, text=text, question=question)
                if created:
                    logger.info(f"Progress for student {self.telegram_id} saved successfully.")
                return progress, created
            except (IntegrityError, PeeweeException) as e:
                logger.error(f"Error saving progress for student {self.telegram_id}: {e}")
                raise e

    def get_progress(self):
        try:
            progress = Progress.select().where(Progress.student == self)
            return progress
        except PeeweeException as e:
            logger.error(f"Error getting progress for student {self.telegram_id}: {e}")
            raise e

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
    question = ForeignKeyField(Question, backref='answers')
    answer = TextField()

class Teacher(BaseModel):
    name = CharField(max_length=100)

class Progress(BaseModel):
    student = ForeignKeyField(Student, backref='progress')
    text = ForeignKeyField(Text, backref='progress')
    question = ForeignKeyField(Question, backref='progress')

if __name__ == "__main__":
    db.connect()
    db.create_tables([Text, Question, Student, Answer, Teacher, Progress], safe=True)
