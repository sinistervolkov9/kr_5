# Взаимодействие пользователя с программой

from settings import get_employer_str


class Interaction:
    def interactive_start(self):
        """
        pass
        :return: str
        """
        print("Привет!")
        print(f"Вот список компаний, вакансии в которых я буду искать:")
        get_employer_str()
        print("\nБазово я веду поиск по всей России, но если Вас интересуют вакансии компаний в конкретном регионе, то введиnt его")
        print("Если это не важно, то просто нажмите ENTER\n")

        area = str(input()).title().strip()
        if area == "":
            return "Россия"
        else:
            return area
