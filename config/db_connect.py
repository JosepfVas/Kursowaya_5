from src.db_manager import DBManager


def get_db_manager():
    """ Функция возвращает наши данные для подключения к БД. """
    return DBManager(
        host='localhost',
        database='kyrsowaya5',
        user='postgres',
        password='852467913'
    )
