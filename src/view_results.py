import math

import src.utils_hh
import json
import src.vacancies


class ViewResults:

    def __init__(self):
        self.current_page = 1
        self.max_page = 1
        self.results_on_page = 10
        self.commands_list = ['0', '1', '2']

        self.result_dict = []
        self.view_vacancy_objects_dict = []

        self.location_filter = ''
        self.salary_from_filter = ''
        self.salary_to_filter = ''
        self.key_words_filter = []

        self.load_data()
        self.filter_view_data()
        self.view_data()

    def load_data(self):
        self.current_page = 1

        file_path = 'data/vacancies.json'
        file_worker = src.utils_hh.FileWorker(file_path)
        hh_parser = src.utils_hh.HH(file_worker)

        # Загрузка вакансий по ключевому слову
        hh_parser.load_vacancies(input('Введите профессию для запроса с сайта\n'))

        with open(file_path, 'r', encoding='utf-8') as file:
            self.result_dict = json.load(file)

    def filter_view_data(self):
        self.view_vacancy_objects_dict.clear()
        for vac in self.result_dict:
            vac_obj = src.vacancies.VacancyObject(vac)
            if self.location_filter == '' or self.location_filter == vac_obj.location:
                self.view_vacancy_objects_dict.append(vac_obj)

        self.max_page = math.ceil(len(self.view_vacancy_objects_dict) / self.results_on_page)

    def view_data(self):
        while 1 == 1:
            for i in range((self.current_page - 1) * self.results_on_page, self.current_page * self.results_on_page, 1):
                print(self.view_vacancy_objects_dict[i].salary_from)
                self.view_vacancy_objects_dict[i].display()
            current_command = 'r'
            while current_command not in self.commands_list:
                current_command = input('1 - Дальше   2 - Назад   0 - Настройки\n')
            if current_command == '1':
                self.switch_page(1)
            elif current_command == '2':
                self.switch_page(-1)
            elif current_command == '0':
                self.view_settings()

    def switch_page(self, increment):
        self.current_page += int(increment)
        if self.current_page < 1:
            self.current_page = 1
        elif self.current_page > self.max_page:
            self.current_page = self.max_page

    def view_settings(self):
        current_command = ""
        set_commands_list = ['1', '2', '3', '4', '5', '0']
        while current_command != '0':
            while current_command not in set_commands_list:
                current_command = input('1 - Город   2 - Зарплата   3 - Ключевые слова   4 - Элементы на странице   5 '
                                        '- Новый запрос   0 - Готово\n')
            if current_command == '1':
                self.set_location_filter()
            if current_command != '0':
                current_command = 'n'
        self.filter_view_data()

    def set_location_filter(self):
        self.location_filter = input('Введите название города. (Оставьте пустое поле для всех.) \n')
