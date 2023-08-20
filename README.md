# Курсовой проект "Парсер данных о вакансиях"

Проект представляет собой программу для парсинга данных о вакансиях и компаниях с сайта hh.ru и их загрузки в базу данных PostgreSQL. 
Также в проекте реализована возможность выполнения запросов к базе данных для получения информации о компаниях и вакансиях. 
Вам доступны запросы к базе данных для получения информации о компаниях, вакансиях, средней зарплате и другой статистике.

## Как запустить проект

1. Создайте базу данных в PostgreSQL с именем "Parser_hh" (или измените параметры подключения в коде).
2. Выберите компании, вакансии которых вы хотите просмотреть. Заходите на сайт hh.ru, находите заинтересовавшую вас компанию,
  заходите на главную страницу работодателя\компании на сайте, смотрите ссылку страницы (пример https://hh.ru/employer/581458) цифры в конце - id компании.
  id вставляете в список company_ids в начале main.py (Там указано в # куда надо вводить id)
3. Запустите скрипт main.py

## Как использовать программу

1. При запуске программы вам будет предоставлено меню с доступными действиями:

- "Получить данные о компаниях и вакансиях с hh.ru и загрузить их в БД"
- "Выполнить запросы к базе данных"
- "Очистить базу данных"
- "Выход из программы"

2. Выберите нужное действие, следуя указаниям программы.

### Замечание

- Загрузка данных о вакансиях может занять некоторое время в зависимости от количества вакансий у указанных компаний.
