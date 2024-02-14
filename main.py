from settings import companies_list, get_employer_id, config
from api import HeadHunterAPI
from interaction import Interaction
from db_manager import DBUtils

# Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.


class Main:
    def __init__(self):
        self.new_search()
        self.companies_list = companies_list
        self.params = config()

    def new_search(self):
        self.request_hh = HeadHunterAPI()
        self.interaction = Interaction()
        self.db_utils = DBUtils()

    def run(self):
        self.db_utils.create_db("hh", self.params)
        self.db_utils.create_tabs(self.params)
        search_area = self.interaction.interactive_start()
        for i in range(len(self.companies_list)):
            print(i+1)
            #self.request_hh.get_request(get_employer_id()[i], search_area)
            data = self.request_hh.get_request(get_employer_id()[i], search_area)
            self.db_utils.record(data, self.params)


if __name__ == '__main__':
    main = Main()
    main.run()

# params = config()
# db_utils = DBUtils()
# db_utils.create_db("hh", params)
# db_utils.create_tabs(params)
