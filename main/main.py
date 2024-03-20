import os
from config.employer_ids import load_employer_ids
from sql_requests.sql_tables import create_tables, fill_vacancies, fill_employers
from src.db_manager import DBManager
from src.hh_api import HHApi

TOKEN = "USERLVV0TNLUJNURIM02P88L5EPBJ00TBF9AJDQCP8VDEJ7K2DOSPKNA0DLT4HE0"

if __name__ == "__main__":
    db_manager = DBManager(
        host='localhost',
        database='kyrsowaya5',
        user='postgres',
        password='852467913'
    )

    conn = db_manager.connect()
    hh_api = HHApi(TOKEN)

    file_path = os.path.join('..', 'config', 'employers_id.txt')
    employer_id = load_employer_ids(file_path)

    vacancies = hh_api.get_employer_vacancies(employer_id)
    employer_info = hh_api.get_employer_info(vacancies)

    employer_data = []
    vacancy_data = []

    for info in employer_info:
        employer_data.append((info['employer_name'], info['employer_url'], info['employer_id']))
        vacancy_data.append((info['vacancy_name'], info['vacancy_id'], info['employer_id'], info['salary_from'],
                             info['salary_to'], info['vacancy_url']))

    unique_employer_data = set(employer_data)

    create_tables(conn)
    fill_employers(conn, unique_employer_data)
    fill_vacancies(conn, vacancy_data)

    print("Таблицы созданы и заполнены данными")

    while True:
        print("\nВыберите действие:")
        print("1. Список всех компаний и количество вакансий у каждой компании.")
        print("2. Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на "
              "вакансию.")
        print("3. Получить среднюю зарплату по вакансиям.")
        print("4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.")
        print("5. Получить список всех вакансий, по вашему запросу")
        print("6. Выход")

        user_choice = input("Введите номер действия: ")

        if user_choice == "1":
            result = db_manager.get_companies_and_vacancies_count(conn)
            for company, vacancies_count in result:
                print(f"Компания: {company}, Количество вакансий: {vacancies_count}")
        elif user_choice == "2":
            result = db_manager.get_all_vacancies(conn)
            for company, vacancy_name, salary_from, salary_to, vacancy_url in result:
                print(f"Компания: {company}, Вакансия: {vacancy_name}, Зарплата от: {salary_from}руб., "
                      f"Зарплата до: {salary_to}руб., Ссылка: {vacancy_url}")
        elif user_choice == "3":
            result = db_manager.get_avg_salary(conn)
            print(f"Средняя зарплата по вакансиям {round(result)}руб.")
        elif user_choice == "4":
            result = db_manager.get_vacancies_with_higher_salary(conn)
            for company, vacancy_name, salary_from, salary_to in result:
                print(f"Компания: {company}, Вакансия: {vacancy_name}, Зарплата от: {salary_from}руб., "
                      f"Зарплата до: {salary_to}руб.")
        elif user_choice == "5":
            vacancy_name = input("Введите название вакансии: ")
            result = db_manager.get_vacancies_with_keyword(conn, vacancy_name)
            for company, vacancy_name, salary_from, salary_to, vacancy_url in result:
                print(f"Компания: {company}, Вакансия: {vacancy_name}, Зарплата от: {salary_from}руб., "
                      f"Зарплата до: {salary_to}руб., Ссылка: {vacancy_url}")
        elif user_choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")
