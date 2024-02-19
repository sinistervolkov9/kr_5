# -------------------------------------------------------- MAIN --------------------------------------------------------

import sys
from settings import companies_list, get_employer_id, config
from api import HeadHunterAPI
from interaction import Interaction
from db_manager import DBUtils, DBManager
from print_helper import PrintHelper


class Main:
    def __init__(self):
        self.new_search()
        self.companies_list = companies_list
        self.params = config()
        self.running = True

    def new_search(self):
        self.request_hh = HeadHunterAPI()
        self.interaction = Interaction()
        self.db_utils = DBUtils()
        self.db_manager = DBManager(self)
        self.printhelper = PrintHelper()

    def run(self):
        self.db_utils.create_db("hh", self.params)
        self.db_utils.create_tabs(self.params)
        search_area = self.interaction.interactive_start()
        print("Загрузка...")
        for i in range(len(self.companies_list)):
            print(f"{i + 1}/{len(self.companies_list)}")
            data = self.request_hh.get_request(get_employer_id()[i], search_area)
            for i in data:
                conv_data = self.db_utils.converter(i)
                self.db_utils.record(conv_data[0], conv_data[1], self.params)
        self.interaction.print_database_is_formed()
        while self.running:
            user_input = self.interaction.actions()
            if user_input == "q":
                self.running = False
                sys.exit()
            elif user_input == "1":
                self.db_manager.get_companies_and_vacancies_count(self.params)
            elif user_input == "2":
                self.db_manager.get_all_vacancies(self.params)
            elif user_input == "3":
                self.db_manager.get_avg_salary(self.params)
            elif user_input == "4":
                self.db_manager.get_vacancies_with_higher_salary(self.params)
            elif user_input == "5":
                self.db_manager.get_vacancies_with_keyword(self.params)
            else:
                self.printhelper.no_comand()


if __name__ == '__main__':
    main = Main()
    main.run()
