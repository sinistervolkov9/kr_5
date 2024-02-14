import psycopg2


class DBUtils:
    def create_db(self, database_name, params):
        """создание БД"""

        connection = self.connection(params)  # psycopg2.connect(dbname="postgres", **params)
        cur = connection.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")
        self.connection_close(connection)

    def create_tabs(self, params):
        """создание таблиц"""

        connection = self.connection(params,
                                     database_name="hh")  # вызываем метод соединения с указанием имени базы данных
        with connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancy (
                    vacancy_id INTEGER,
                    vacancy_name VARCHAR(255),
                    region_id INTEGER,
                    region VARCHAR(255),
                    salary_from INTEGER,
                    salary_to INTEGER,
                    city VARCHAR(255),
                    street VARCHAR(255),
                    building VARCHAR(255),
                    published_at DATE,
                    url VARCHAR(1000),
                    employer_id INTEGER,
                    employer_name VARCHAR(255),
                    employer_url VARCHAR(255),
                    requirement VARCHAR(255),
                    responsibility VARCHAR(255),
                    experience VARCHAR(255),
                    employment VARCHAR(255)
                )
            """)

        self.connection_close(connection)  # вызываем метод закрытия соединения

    def connection(self, params, database_name="postgres"):
        """метод соединения (см. картинку)"""

        connect = psycopg2.connect(dbname=database_name, **params)  # создаем соединение с базой данных
        connect.autocommit = True  # включаем режим автоматической фиксации
        return connect  # возвращаем соединение

    def connection_close(self, connection):
        """метод закрытия соединения (см. картинку)"""
        connection.commit()
        connection.close()

    def record(self, data, params):
        """add_data_to_tabs
        заполнить данными таблицу"""

        connection = self.connection(params, database_name="hh")
        with connection.cursor() as cur:
            for i in data:
                id = i["id"] if i["id"] is not None else 0
                name = i["name"] if i["name"] is not None else ""
                area_id = i["area"]["id"] if i["area"]["id"] is not None else 0
                area_name = i["area"]["name"] if i["area"]["name"] is not None else ""
                salary = i["salary"] if i["salary"] is not None else {"from": None, "to": None}
                salary_from = salary["from"] if salary["from"] is not None else 0
                salary_to = salary["to"] if salary["to"] is not None else 0
                address = i["address"] if i["address"] is not None else {"city": None, "street": None, "building": None}
                city = address["city"] if address["city"] is not None else ""
                street = address["street"] if address["street"] is not None else ""
                building = address["building"] if address["building"] is not None else ""
                published_at = i["published_at"] if i["published_at"] is not None else ""
                url = i["alternate_url"] if i["alternate_url"] is not None else ""
                employer = i["employer"] if i["employer"] is not None else {"id": None, "name": None,
                                                                            "alternate_url": None}
                employer_id = employer["id"] if employer["id"] is not None else ""
                employer_name = employer["name"] if employer["name"] is not None else ""
                employer_url = employer["alternate_url"] if employer["alternate_url"] is not None else ""
                snippet = i["snippet"] if i["snippet"] is not None else {"requirement": None, "responsibility": None}
                requirement = snippet["requirement"] if snippet["requirement"] is not None else ""
                responsibility = snippet["responsibility"] if snippet["responsibility"] is not None else ""
                experience = i["experience"] if i["experience"] is not None else {"experience_name": None}
                experience_name = experience["name"] if experience["name"] is not None else ""
                employment = i["employment"] if i["employment"] is not None else {"employment_name": None}
                employment_name = employment["name"] if employment["name"] is not None else ""

                cur.execute("""
insert into vacancy values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            [id, name, area_id, area_name, salary_from, salary_to, city, street, building, published_at,
                             url, employer_id,
                             employer_name, employer_url, requirement, responsibility, experience_name,
                             employment_name])

        self.connection_close(connection)


class DBManager:
    # Создайте класс DBManager, который будет подключаться к БД PostgreSQL и иметь следующие методы:
    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании.
        """
        pass

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
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
