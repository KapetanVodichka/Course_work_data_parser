from func import get_all_vacancies, get_companies, get_vacancies, clear_database
from DBManager import DBManager
from Data_insert import insert_companies, insert_vacancies, conn

# Здесь укажите ваши данные для подключения к БД
DB_HOST = 'localhost'
DB_NAME = 'Parser_hh'
DB_USER = 'postgres'
DB_PASSWORD = '****'

# Тут укажите id компаний, по которым ищете вакансии
company_ids = [78638, 882, 9538510, 32737, 49357, 3093544, 39305, 205, 4275908, 581458]


def main():
    db_manager = None
    while True:
        print("\n1. Получить данные о компаниях и вакансиях с hh.ru и загрузить их в БД")
        print("2. Выполнить запросы к базе данных")
        print("3. Очистить базу данных")
        print("4. Выход из программы")
        choice = input("Выберите действие: ")

        if choice == "1":
            print('В зависимости от количества вакансий сбор информации о вакансиях может занять до 1 минуты')
            # Получение данных о вакансиях с сайта hh.ru
            vacancies_data = get_all_vacancies(company_ids)

            # Подключение к БД и использование DBManager
            db_manager = DBManager(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
            db_manager.create_tables()  # Создание таблиц

            # Загрузка данных о компаниях
            companies_data = get_companies(company_ids)
            insert_companies(db_manager.conn, companies_data)

            # Загрузка данных о вакансиях
            for company_id in company_ids:
                vacancies = get_vacancies(company_id)
                insert_vacancies(db_manager.conn, vacancies)

            print("Данные успешно загружены в базу данных.")
            db_manager.close()

        elif choice == "2":
            db_manager = DBManager(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)

            print("\n1. Получить список всех компаний и количество вакансий")
            print("2. Получить список всех вакансий")
            print("3. Получить среднюю зарплату")
            print("4. Получить вакансии с зарплатой выше средней")
            print("5. Поиск вакансий по ключевому слову")
            query_choice = input("Выберите запрос (1/2/3/4/5): ")

            if query_choice == "1":
                companies_vacancies = db_manager.get_companies_and_vacancies_count()
                print("\nСписок компаний и количество вакансий:")
                for company in companies_vacancies:
                    print(f"id {company[0]} - {company[1]} - {company[2]} вакансий")

            elif query_choice == "2":
                all_vacancies = db_manager.get_all_vacancies()
                print("\nСписок всех вакансий:")
                for vacancy in all_vacancies:
                    print(f"{vacancy[0]} - {vacancy[1]} - Зарплата: {vacancy[2]} - {vacancy[3]}, ссылка: {vacancy[4]}")

            elif query_choice == "3":
                avg_salary = db_manager.get_avg_salary()
                print(f"\nСредняя зарплата: {avg_salary}")

            elif query_choice == "4":
                high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
                print("\nСписок вакансий с зарплатой выше средней:")
                for vacancy in high_salary_vacancies:
                    print(f"{vacancy[0]} - {vacancy[1]} - Зарплата: {vacancy[2]} - {vacancy[3]}, ссылка: {vacancy[5]}")

            elif query_choice == "5":
                keyword = input("\nВведите ключевое слово: ")
                keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
                print(f"Список вакансий с ключевым словом '{keyword}':")
                for vacancy in keyword_vacancies:
                    company_name = vacancy[0]
                    company_id = vacancy[1]
                    title = vacancy[2]
                    salary_from = vacancy[3]
                    salary_to = vacancy[4]
                    currency = vacancy[5]
                    link_page = vacancy[6]

                    print(f"\nНазвание компании: {company_name}")
                    print(f"id компании: {company_id}")
                    print(f"Должность: {title}")

                    if salary_from is not None:
                        print(f"Зарплата:\n    От: {salary_from}")
                    else:
                        print(f"Зарплата:\n    От: Не указано")

                    if salary_to is not None:
                        print(f"    До: {salary_to}")
                    else:
                        print(f"    До: Не указано")

                    if currency is not None:
                        print(f"Валюта: {currency}")
                    else:
                        continue

                    print(f"Ссылка: {link_page}")

            db_manager.close()

        elif choice == "3":
            db_manager = DBManager(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
            clear_database(db_manager)

        elif choice == "4":
            print("Выход из программы.")
            db_manager.close()
            break

        else:
            print("Неправильный выбор.")

if __name__ == '__main__':
    main()