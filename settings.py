# import os
from configparser import ConfigParser

# PASSWORD = os.getenv("My_PostgreSQL_password")
companies_list = [
    {
        "Магнит": 49357
    },
    {"Тинькофф": 78638
     },
    {"lamoda": 780654
     },
    {"Пятёрочка": 1942330
     },
    {"Ozon": 2180
     },
    {"DNS": 1025275
     },
    {"Яндекс": 1740
     },
    {"ООО ЛИИС": 9702242
     },
    {"Спортмастер": 2343
     },
    {"Burger King": 625332
     }
]


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def get_employer_id():
    id_list = []
    for i in companies_list:
        for key, value in i.items():
            id_list.append(value)
    return id_list


def get_employer_str():
    for i in companies_list:
        for key, value in i.items():
            print(key)
