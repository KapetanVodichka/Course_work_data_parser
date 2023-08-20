import psycopg2


class DBManager:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """
        Создание таблиц в БД
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                company_id INTEGER UNIQUE
);
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                company_id INTEGER REFERENCES companies(company_id),
                title TEXT NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                currency TEXT,
                link_page TEXT
            );
        """)
        self.conn.commit()

    def drop_tables(self):
        """
        Удаление таблиц
        """
        self.cursor.execute("DROP TABLE IF EXISTS vacancies")
        self.cursor.execute("DROP TABLE IF EXISTS companies")
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """
        Возвращает количество вакансий у каждой компании
        """
        self.cursor.execute("SELECT companies.company_id, companies.name, COUNT(vacancies.id) FROM vacancies "
                            "LEFT JOIN companies USING(company_id) "
                            "GROUP BY companies.company_id, companies.name")
        companies_and_vacancies = self.cursor.fetchall()
        return companies_and_vacancies

    def get_all_vacancies(self):
        """
        Возвращает вакансии всех указанных компаний
        """
        self.cursor.execute("SELECT companies.name, vacancies.title, salary_from, salary_to, vacancies.link_page FROM vacancies "
                            "JOIN companies USING(company_id)")
        all_vacancies = self.cursor.fetchall()
        return all_vacancies

    def get_avg_salary(self):
        """
        Возвращает среднюю зарплату всех вакансий (вакансии без указания зарплаты не учитываются)
        """
        self.cursor.execute(
            "SELECT ROUND(AVG(CASE WHEN (salary_from IS NULL OR salary_from = 0) THEN salary_to ELSE COALESCE(salary_from, 0) END), 1) FROM vacancies"
        )
        avg_salary = self.cursor.fetchone()[0]
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """
        Возвращает вакансии с зарплатой выше средней по всем вакансиям
        """
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            "SELECT companies.name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.currency, vacancies.link_page "
            "FROM vacancies "
            "JOIN companies USING(company_id) "
            "WHERE (vacancies.salary_from > %s OR vacancies.salary_to > %s) AND vacancies.salary_from IS NOT NULL",
            (avg_salary, avg_salary))
        high_salary_vacancies = self.cursor.fetchall()
        return high_salary_vacancies

    def get_vacancies_with_keyword(self, keyword):
        """
        Возвращает вакансии по ключевым словам в названии
        """
        keyword = f"%{keyword}%"
        self.cursor.execute(
            "SELECT companies.name, vacancies.company_id, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.currency, vacancies.link_page FROM vacancies "
            "JOIN companies USING(company_id) "
            "WHERE vacancies.title ILIKE %s", (keyword,))
        keyword_vacancies = self.cursor.fetchall()
        return keyword_vacancies

    def close(self):
        self.cursor.close()
        self.conn.close()
