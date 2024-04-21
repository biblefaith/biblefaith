from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('bot.db')


class ModelBase(pw.Model):
    created_at = pw.DateTimeField(default=datetime.now, formats=['%Y-%m-%d %H:%M:%S.%f'])

    class Meta():
        legacy_table_names=False
        database = db


class BibleTranslations(ModelBase):
    name = pw.CharField(max_length=50)
    description = pw.CharField(max_length=100)


class UserLevels(ModelBase):
    name = pw.CharField(max_length=50)
    description = pw.CharField(max_length=100)

class UserSettings(ModelBase):
    telegram_id = pw.IntegerField(primary_key=True)
    bible_translation = pw.ForeignKeyField(BibleTranslations, backref='user_settings')
    user_level = pw.ForeignKeyField(UserLevels, backref='user_settings')

