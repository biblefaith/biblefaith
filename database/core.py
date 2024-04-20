from common.models import db, BibleTranslations, UserLevels


def init_database():

    with db.atomic():
        if not BibleTranslations.table_exists():
            db.create_tables([BibleTranslations])
            BibleTranslations.create(name = "RST+", description = "TBD")
            BibleTranslations.create(name = "NRT", description = "Новый Русский Перевод (НРП)")

        if not UserLevels.table_exists():
            db.create_tables([UserLevels])
            UserLevels.create(name = "beginner", description = "Начинающий")
            UserLevels.create(name = "advanced", description = "Продвинутый")

        query = BibleTranslations.delete().where(BibleTranslations.name == "test")
        query.execute()
