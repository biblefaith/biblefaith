from common.models import db, BibleTranslations, UserLevels, UserSettings


def create_table_if_not_exists(table, data=None):
    if not table.table_exists():
        db.create_tables([table])
        if data:
            for row_data in data:
                table.create(**row_data)

def init_database():
    with db.atomic():
        create_table_if_not_exists(BibleTranslations, [
            {"name": "RST+", "description": "TBD"},
            {"name": "NRT", "description": "Новый Русский Перевод (НРП)"}
        ])

        create_table_if_not_exists(UserLevels, [
            {"name": "beginner", "description": "Начинающий"},
            {"name": "advanced", "description": "Продвинутый"}
        ])

        create_table_if_not_exists(UserSettings)

if __name__ == '__main__':
    init_database()
    UserSettings.create(telegram_id=123, bible_translation=BibleTranslations.get(BibleTranslations.name == "RST+"), user_level=UserLevels.get(UserLevels.name == "beginner"))