import requests


def get_companies(interesting_company_ids):
    """
    Получение данных о компаниях
    """
    companies_data = []
    for company_id in interesting_company_ids:
        url = f'https://api.hh.ru/employers/{company_id}'
        response = requests.get(url)
        company_data = response.json()
        companies_data.append(company_data)
    return companies_data


def get_vacancy_count(company_id):
    """
    Получение количества вакансий для компании
    """
    url = f'https://api.hh.ru/vacancies?employer_id={company_id}&per_page=100'
    response = requests.get(url)
    vacancies_data = response.json()
    return vacancies_data['found']


def get_vacancies(company_id, max_vacancies=None):
    per_page = 100
    page = 0
    all_vacancies = []

    while True:
        url = f'https://api.hh.ru/vacancies'
        params = {'employer_id': company_id, 'per_page': per_page, 'page': page}
        response = requests.get(url, params=params)
        vacancies_data = response.json()

        if 'items' in vacancies_data:
            vacancies = vacancies_data['items']
            all_vacancies.extend(vacancies)

            if len(vacancies) < per_page or (max_vacancies is not None and len(all_vacancies) >= max_vacancies):
                break

        else:
            break

        page += 1

    return all_vacancies[:max_vacancies] if max_vacancies is not None else all_vacancies


def get_all_vacancies(company_ids):
    """
    Получение данных о вакансиях всех указанных компаний
    """
    all_vacancies = []

    for company_id in company_ids:
        vacancies = get_vacancies(company_id, max_vacancies=500)
        all_vacancies.extend(vacancies)

    return all_vacancies


def clear_database(db_manager):
    """
    Чистка базы данных
    """
    choice = input("Вы уверены, что хотите очистить базу данных? (y/n): ")
    if choice.lower() == "y":
        db_manager.drop_tables()
        print("Таблицы успешно удалены из базы данных.")
        db_manager.close()
    else:
        print("Отмена операции.")
