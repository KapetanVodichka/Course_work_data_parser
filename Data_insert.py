import psycopg2

# Данные для входа в Базу Данных
DB_HOST = 'localhost'
DB_NAME = 'Parser_hh'
DB_USER = 'postgres'
DB_PASSWORD = '****'

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def insert_companies(conn, companies):
    """
    Загрузка данных о компаниях в таблицу companies
    """
    cursor = conn.cursor()

    for company in companies:
        cursor.execute("INSERT INTO companies (name, company_id) VALUES (%s, %s)",
                       (company['name'], company['id']))
    conn.commit()


def insert_vacancies(conn, vacancies_data):
    """
    Загрузка данных о вакансиях в таблицу vacancies
    """
    cursor = conn.cursor()

    for vacancy in vacancies_data:
        company_id = vacancy['employer']['id']
        title = vacancy['name']
        salary_from = vacancy['salary']['from'] if vacancy['salary'] else None
        salary_to = vacancy['salary']['to'] if vacancy['salary'] else None
        currency = vacancy['salary']['currency'] if vacancy['salary'] else None
        link = vacancy['alternate_url']

        cursor.execute("INSERT INTO vacancies (company_id, title, salary_from, salary_to, currency, link_page) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (company_id, title, salary_from, salary_to, currency, link))

    conn.commit()

    cursor.close()
