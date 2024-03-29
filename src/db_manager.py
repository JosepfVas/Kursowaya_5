import psycopg2


class DBManager:
    """ Класс для подключения/отключения от ДБ, работы с ним и манипулировать данными. """
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        """ Метод, для подключения к ДБ. """
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

        return self.conn

    def disconnect(self):
        """ Метод, для отключения от ДБ. """
        if self.conn:
            self.conn.close()

    @staticmethod
    def get_companies_and_vacancies_count(conn):
        """ Метод, который возвращает нам количество вакансий у каждой компании. """
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT employers.name,"
                            "COUNT(vacancies.employer_id) as vacancy_count "
                            "FROM employers "
                            "LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id "
                            "GROUP BY employers.name")
                companies_and_vacancies = cur.fetchall()
                return companies_and_vacancies
        except psycopg2.Error as e:
            raise RuntimeError("Ошибка при выполнении запроса:", e)

    @staticmethod
    def get_all_vacancies(conn):
        """ Метод, который возвращает нам все вакансии. """
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT employers.name, vacancies.vacancy_name, vacancies.salary_from, "
                            "vacancies.salary_to, vacancies.vacancy_url "
                            "FROM vacancies "
                            "JOIN employers ON employers.employer_id = vacancies.employer_id")
                all_vacancies = cur.fetchall()
                return all_vacancies
        except psycopg2.Error as e:
            raise RuntimeError("Ошибка при выполнении запроса:", e)

    @staticmethod
    def get_avg_salary(conn):
        """ Возвращает среднюю зарплату по вакансиям. """
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary_from + salary_to) / 2 as avg_salary "
                            "FROM vacancies")
                avg_salary = cur.fetchone()[0]
                return avg_salary
        except psycopg2.Error as e:
            raise RuntimeError("Ошибка при выполнении запроса:", e)

    @staticmethod
    def get_vacancies_with_higher_salary(conn):
        """ Возвращает вакансии самой высокой зарплатой относительно средней зарплаты. """
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT name, vacancy_name, salary_from, salary_to "
                            "FROM employers, vacancies "
                            "WHERE (salary_from + salary_to) / 2 > (SELECT AVG(salary_from + salary_to) / 2 FROM "
                            "vacancies)")
                vacancies_with_higher_salary = cur.fetchall()
                return vacancies_with_higher_salary
        except psycopg2.Error as e:
            raise RuntimeError("Ошибка при выполнении запроса:", e)

    @staticmethod
    def get_vacancies_with_keyword(conn, keyword):
        """ Возвращает вакансии по ключевому слову. """
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT employers.name, vacancies.vacancy_name, vacancies.salary_from,"
                            "vacancies.salary_to, vacancies.vacancy_url "
                            "FROM vacancies "
                            "JOIN employers ON employers.employer_id = vacancies.employer_id "
                            "WHERE vacancies.vacancy_name LIKE %s", ('%' + keyword + '%',))
                vacancies_with_keyword = cur.fetchall()
                return vacancies_with_keyword
        except psycopg2.Error as e:
            raise RuntimeError("Ошибка при выполнении запроса:", e)
