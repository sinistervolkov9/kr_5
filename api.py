# -------------------------- Получение данных о работодателях и их вакансиях с сайта hh.ru -----------------------------
# ---------------------------------------------- Подключение по API ----------------------------------------------------

import json
import requests
from abc import ABC, abstractmethod


class Api(ABC):
    """
    Класс для работы с API сайтов с вакансиями
    """

    @abstractmethod
    def get_request(self, employer_id, per_page):
        pass


class HeadHunterAPI(Api):
    """
    Класс для работы с платформой hh.ru;
    Поиск вакансий по названию компании
    """

    def get_area_id(self, area_name):
        """
        Преобразования региона поиска из строчного вида в числовой
        (для корректной работы программы)
        """

        url = "https://api.hh.ru/areas"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)

            for region in data:
                if region["name"].title().strip() == area_name.title().strip():
                    return region["id"]
                else:
                    continue

            for region in data:
                for region_areas in region["areas"]:
                    if region_areas["name"].title().strip() == area_name.title().strip():
                        return region_areas["id"]
                    else:
                        continue

            for region in data:
                for region_areas in region["areas"]:
                    for city in region_areas["areas"]:
                        if city["name"].title().strip() == area_name.title().strip():
                            return city["id"]
                        else:
                            continue

        else:
            return None

    def get_request(self, employer_id, area_name, per_page=25):
        """
        Производится запрос к hh.ru
        на получение вакансий в указанном регионе
        """

        area_id = self.get_area_id(area_name)

        if area_id:
            url = "https://api.hh.ru/vacancies/"
            params = {"employer_id": employer_id, "area": area_id, "page": 0, "per_page": per_page}
            request = requests.get(url, params=params)
            return request.json()["items"]
        else:
            return []
