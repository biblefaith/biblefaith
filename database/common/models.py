from loguru import logger
from peewee import Model, SqliteDatabase, DateTimeField, CharField, TextField, ForeignKeyField, BooleanField, IntegerField, IntegrityError, PeeweeException
from datetime import datetime, timezone

logger.add("debug.log", rotation="10 MB", compression="zip")
db = SqliteDatabase('bot.db')

class BaseModel(Model):
    created_at = DateTimeField(default=lambda: datetime.now())

    class Meta:
        database = db
        legacy_table_names = False

class Student(BaseModel):
    telegram_id = IntegerField(unique=True)
    telegram_full_name = CharField(max_length=100, null=True)
    telegram_username = CharField(max_length=100, null=True)
    status = BooleanField(default=True)
    text_type = CharField(max_length=20, null=True)
    question_type = CharField(max_length=20, null=True)
    day_number = IntegerField(default=1)
    ordering_number = IntegerField(default=1)


    @classmethod
    @logger.catch
    def create_or_update(cls, telegram_id, **kwargs):
        with cls._meta.database.atomic():  # Start transaction
            student, created = cls.get_or_create(telegram_id=telegram_id)
            for key, value in kwargs.items():
                if getattr(student, key, None) != value:
                    setattr(student, key, value)
            student.save()
            return student, created


class Answer(BaseModel):
    telegram_id = IntegerField()
    day_number = IntegerField()
    question_number = IntegerField()
    answer = TextField()

class Teacher(BaseModel):
    telegram_id = IntegerField(unique=True)
    telegram_full_name = CharField(max_length=100, null=True)
    telegram_username = CharField(max_length=100, null=True)

class Diary(Model):

    class Meta:
        database = db

    day_number = IntegerField()
    content_ordering_value = IntegerField()
    content_value = TextField()
    content_variety = CharField(max_length=20) # advanced | beginner | rst | nrt
    content_category = CharField(max_length=20) # question | bible
    created_at = DateTimeField(default=lambda: datetime.now())


class UserMessage(BaseModel):
    telegram_id = IntegerField()
    message = TextField()


if __name__ == "__main__":
    db.connect()
    db.create_tables([Diary, Student, Answer, Teacher], safe=True)
