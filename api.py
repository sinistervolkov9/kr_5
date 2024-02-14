import json
import requests
from abc import ABC, abstractmethod


# Получить данные о работодателях и их вакансиях с сайта hh.ru.
# Для этого используйте публичный API hh.ru и библиотеку requests.

class Api(ABC):
    """
    Класс для работы с API сайтов с вакансиями.
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

        # Формируем URL для получения списка регионов
        url = "https://api.hh.ru/areas"

        # Отправляем запрос и получаем ответ
        response = requests.get(url)

        # Проверяем статус ответа
        if response.status_code == 200:
            # Преобразуем ответ в формат JSON
            data = json.loads(response.text)

            # Ищем id региона по его названию
            for region in data:
                if region["name"].title().strip() == area_name.title().strip():
                    print(region["id"])
                    return region["id"]
                else:
                    continue

            for region in data:
                for region_areas in region["areas"]:
                    if region_areas["name"].title().strip() == area_name.title().strip():
                        print(region_areas["id"])
                        return region_areas["id"]
                    else:
                        continue

            for region in data:
                for region_areas in region["areas"]:
                    for city in region_areas["areas"]:
                        if city["name"].title().strip() == area_name.title().strip():
                            print(city["id"])
                            return city["id"]
                        else:
                            continue
        else:
            # Если статус ответа не 200, возвращаем None
            return None

    def get_request(self, employer_id, area_name, per_page=5):
        """123"""
        # Получаем id региона по названию
        area_id = self.get_area_id(area_name)

        # Если id региона найден, формируем запрос к API
        if area_id:
            url = "https://api.hh.ru/vacancies/"
            params = {"employer_id": employer_id, "area": area_id, "page": 0, "per_page": per_page}

            request = requests.get(url, params=params)
            #print(request.json()["items"])
            return request.json()["items"]
        else:
            # Если id региона не найден, возвращаем пустой список
            return []
