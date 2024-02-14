# Создать класс DBManager для работы с данными в БД.
# Класс DBManager должен использовать библиотеку psycopg2 для работы с БД.

import psycopg2

class DBManager:
    def create_db(self):
        """
        создание БД
        """
        pass

    def create_tabs(self):
        """
        создание таблиц
        """
        pass

    def connection(self):
        """
        метод соединения (см. картинку)
        """
        pass

    def connection_close(self):
        """
        метод закрытия соединения (см. картинку)
        """
        pass

    # Создайте класс DBManager, который будет подключаться к БД PostgreSQL и иметь следующие методы:
    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании.
        """
        pass

    def get_all_vacancies(self):
        """
        получает список всехвакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        pass

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """"
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        pass


    def get_vacancies_with_keyword(self):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        pass

    def inserting_data(self):
        """
        вставка данных
        """
        pass
