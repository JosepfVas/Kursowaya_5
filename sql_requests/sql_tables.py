import psycopg2


def create_tables(conn):
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE employers (id SERIAL PRIMARY KEY,"
                            "name VARCHAR(50),"
                            "employee_url VARCHAR(100),"
                            "employer_id INT UNIQUE)")

                cur.execute("CREATE TABLE vacancies (id SERIAL PRIMARY KEY,"
                            "vacancy_name VARCHAR(100),"
                            "vacancy_id INT,"
                            "employer_id INT REFERENCES employers(employer_id),"
                            "salary_from INT,"
                            "salary_to INT,"
                            "vacancy_url VARCHAR(100))")

    except psycopg2.Error as e:
        print("Ошибка при вставке данных:", e)


def fill_employers(conn, emp_data):
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany("INSERT INTO employers (name, employee_url, employer_id) VALUES (%s, %s, %s)", emp_data)
    except psycopg2.Error as e:
        print("Ошибка при вставке данных:", e)


def fill_vacancies(conn, vac_data):
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany("INSERT INTO vacancies (vacancy_name, vacancy_id, employer_id, salary_from,"
                                "salary_to, vacancy_url) VALUES (%s, %s, %s, %s, %s, %s)", vac_data)
    except psycopg2.Error as e:
        print("Ошибка при вставке данных:", e)

