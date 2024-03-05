import psycopg2
from utils.config import config


class DBManager:

    def get_companies_and_vacancies_count(self):
        ''' Метод, получающий список всех компаний и вакансий у каждой компании. '''

        conn = psycopg2.connect(dbname='db_name', **config())

        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT employers.name, COUNT(vacancies.employer_id) AS vacancies_count FROM employers LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id GROUP BY employers.name')
                result = cur.fetchall()
            conn.commit()
        return result


    def get_all_vacancies(self):
        ''' Метод, получающий список всех вакансий. '''

        conn = psycopg2.connect(dbname='db_name', **config())

        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url FROM employers JOIN vacancies using (employer_id)')
                result = cur.fetchall()
            conn.commit()
        return result


    def get_avg_salary(self):
        ''' Метод, получающий среднюю зарплату по вакансиям. '''

        conn = psycopg2.connect(dbname='db_name', **config())

        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT AVG(salary_from) AS payment_avg FROM vacancies')
                result = cur.fetchall()
            conn.commit()
        return result


    def get_vacancies_with_higher_salary(self):
        ''' Метод, получающий список всех вакансий, у которых зарплата выше средней по всем вакансиям. '''

        conn = psycopg2.connect(dbname='db_name', **config())

        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM vacancies WHERE salary_from > (select AVG(salary_from) FROM vacancies)')
                result = cur.fetchall()
            conn.commit()
        return result


    def get_vacancies_with_keyword(self, keywords):
        ''' Метод, поиска всех вакансий по ключевому слову. '''

        conn = psycopg2.connect(dbname='db_name', **config())

        with conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM vacancies WHERE name LIKE \'%{keywords}%\'')
                result = cur.fetchall()
            conn.commit()
        return result