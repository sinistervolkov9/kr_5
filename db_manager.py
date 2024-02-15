# ------------------------------- Файл, содержащий методы управления Базой Данных --------------------------------------

import psycopg2


class DBUtils:
    def create_db(self, database_name, params):
        """
        Создание базы данных
        """

        connection = self.connection(params)  # psycopg2.connect(dbname="postgres", **params)
        cur = connection.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")
        self.connection_close(connection)

    def create_tabs(self, params):
        """
        Создание таблиц
        """

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

        self.connection_close(connection)

    def connection(self, params, database_name="postgres"):
        """
        Подключение программы к базе данных
        """

        connect = psycopg2.connect(dbname=database_name, **params)  # создаем соединение с базой данных
        connect.autocommit = True  # включаем режим автоматической фиксации
        return connect  # возвращаем соединение

    def connection_close(self, connection):
        """
        Прекращение подключения программы к базе данных
        """

        connection.commit()
        connection.close()

    def record(self, data, params):
        """
        add_data_to_tabs
        Заполнение таблицы данными
        """

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


class DBManager(DBUtils):
    def __init__(self, prog):
        self.prog = prog

    def get_companies_and_vacancies_count(self, params):
        """
        Получить список всех компаний и количество вакансий у каждой из них
        """

        connection = self.connection(params, database_name="hh")
        print("Список всех компаний и количество вакансий у каждой из них:")
        with connection.cursor() as cur:
            cur.execute("""
            SELECT employer_name, COUNT(vacancy_id) AS vacancies_count
            FROM vacancy
            GROUP BY employer_name
            ORDER BY vacancies_count DESC
            """)

            results = cur.fetchall()
            for i in results:
                print(f"{i[0]} - {i[1]}")

        self.connection_close(connection)
        self.prog.printhelper.to_return()

    def get_all_vacancies(self, params):
        """
        Получить список всех вакансий с указанием: названия компании, названия вакансии, зарплаты и ссылки на вакансию
        """

        connection = self.connection(params, database_name="hh")
        print("Список всех вакансий:")
        with connection.cursor() as cur:
            cur.execute("""
            SELECT employer_name, vacancy_name, salary_from, salary_to, url
            FROM vacancy
            ORDER BY employer_name, vacancy_name
            """)

            results = cur.fetchall()
            for i in results:
                if i[2] and i[3]:
                    salary = f"{i[2]}-{i[3]}"
                elif i[2]:
                    salary = f"от {i[2]}"
                elif i[3]:
                    salary = f"до {i[3]}"
                else:
                    salary = "Не указана"
                print(f"{i[0]} - {i[1]} - {salary} - {i[4]}")

        self.connection_close(connection)
        self.prog.printhelper.to_return()

    def get_avg_salary(self, params, independence=True):
        """
        Получить среднюю зарплату по вакансиям
        """

        connection = self.connection(params, database_name="hh")
        with connection.cursor() as cur:
            cur.execute("""
            SELECT AVG(COALESCE(salary_from, (salary_from + salary_to) / 2, salary_to, COALESCE(salary_to, 
            (salary_from + salary_to) / 2, salary_from))) AS avg_salary
            FROM vacancy
        """)

            result = round(cur.fetchone()[0], 2)
            if independence:
                print(f"Средняя зарплата по вакансиям - {result}")
            else:
                return result

        self.connection_close(connection)
        if independence:
            self.prog.printhelper.to_return()

    def get_vacancies_with_higher_salary(self, params):
        """"
        Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """

        connection = self.connection(params, database_name="hh")
        with connection.cursor() as cur:
            avg_salary = self.get_avg_salary(params, independence=False)
            cur.execute("""
                        SELECT employer_name, vacancy_name, salary_from, salary_to, url
                        FROM vacancy
                        WHERE COALESCE(salary_from, (salary_from + salary_to) / 2, salary_to, COALESCE(salary_to, 
                        (salary_from + salary_to) / 2, salary_from)) > %s
                        ORDER BY employer_name, vacancy_name
                        """, (avg_salary,))

            results = cur.fetchall()
            for i in results:
                if i[2] and i[3]:
                    salary = f" {i[2]}-{i[3]}"
                elif i[2]:
                    salary = f"от {i[2]}"
                elif i[3]:
                    salary = f"до {i[3]}"
                else:
                    salary = "Не указана"
                print(f"{i[0]} - {i[1]} - зарплата: {salary} - {i[4]}")

        self.connection_close(connection)
        self.prog.printhelper.to_return()

    def get_vacancies_with_keyword(self, params):
        """
        Получить список вакансий по ключевому слову
        """
        connection = self.connection(params, database_name="hh")
        with connection.cursor() as cur:
            keyword = input("Введите ключевое слово для поиска вакансий:\n").strip().lower()
            cur.execute("""
            SELECT employer_name, vacancy_name, salary_from, salary_to, url
            FROM vacancy
            WHERE LOWER(employer_name) LIKE %s
            OR LOWER(vacancy_name) LIKE %s
            OR LOWER(region) LIKE %s
            OR LOWER(city) LIKE %s
            OR LOWER(street) LIKE %s
            OR LOWER(building) LIKE %s
            OR LOWER(employer_url) LIKE %s
            OR LOWER(requirement) LIKE %s
            --OR LOWER(responsibility) LIKE %s
            OR LOWER(experience) LIKE %s
            OR LOWER(employment) LIKE %s
        """, (
                f"%{keyword}%",) * 10)

            results = cur.fetchall()
            for i in results:
                if i[2] and i[3]:
                    salary = f" {i[2]}-{i[3]}"
                elif i[2]:
                    salary = f"от {i[2]}"
                elif i[3]:
                    salary = f"до {i[3]}"
                else:
                    salary = "Не указана"
                print(f"{i[0]} - {i[1]} - зарплата: {salary} - {i[4]}")

        self.connection_close(connection)
        self.prog.printhelper.to_return()
