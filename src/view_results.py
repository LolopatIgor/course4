import math
import json
import src.utils_hh
import src.vacancies

class ViewResults:

    def __init__(self):
        # Инициализация основных переменных
        self.current_page = 1  # Текущая страница
        self.max_page = 1  # Максимальное количество страниц
        self.results_on_page = 10  # Количество результатов на странице
        self.commands_list = ['0', '1', '2']  # Допустимые команды

        # Списки для хранения данных
        self.result_dict = []  # Список всех загруженных вакансий
        self.view_vacancy_objects_dict = []  # Список отфильтрованных вакансий для отображения

        # Параметры фильтрации
        self.location_filter = ''  # Фильтр по местоположению
        self.salary_from_filter = None  # Фильтр по минимальной зарплате
        self.salary_to_filter = None  # Фильтр по максимальной зарплате
        self.key_words_filter = []  # Фильтр по ключевым словам

        # Загрузка данных, фильтрация и отображение
        self.load_data()
        self.filter_view_data()
        self.view_data()

    def load_data(self):
        # Загрузка данных из файла и API
        self.current_page = 1

        file_path = 'data/vacancies.json'
        file_worker = src.utils_hh.FileWorker(file_path)
        hh_parser = src.utils_hh.HH(file_worker)

        # Загрузка вакансий по ключевому слову
        hh_parser.load_vacancies(input('Введите профессию для запроса с сайта\n'))

        # Чтение данных из файла
        with open(file_path, 'r', encoding='utf-8') as file:
            self.result_dict = json.load(file)

    def filter_view_data(self):
        # Фильтрация данных на основе установленных фильтров
        self.view_vacancy_objects_dict.clear()
        for vac in self.result_dict:
            vac_obj = src.vacancies.VacancyObject(vac)

            # Фильтр по местоположению
            if self.location_filter and self.location_filter != vac_obj.location:
                continue

            # Обработка зарплаты, установка значений по умолчанию
            vacancy_salary_from = vac_obj.salary_from if vac_obj.salary_from is not None else 0
            vacancy_salary_to = vac_obj.salary_to if vac_obj.salary_to is not None else 500000

            # Пропуск вакансий без указанной зарплаты, если установлены фильтры по зарплате
            if (self.salary_from_filter or self.salary_to_filter) and (vac_obj.salary_from is None and vac_obj.salary_to is None):
                continue

            # Проверка фильтра по минимальной зарплате
            if self.salary_from_filter and (
                (vacancy_salary_to < self.salary_from_filter and vacancy_salary_to != 0) or
                (self.salary_to_filter and vacancy_salary_from > self.salary_to_filter)
            ):
                continue

            # Проверка фильтра по максимальной зарплате
            if self.salary_to_filter and (
                (vacancy_salary_from > self.salary_to_filter) or
                (self.salary_from_filter and vacancy_salary_to < self.salary_from_filter and vacancy_salary_to != 0)
            ):
                continue

            # Фильтр по ключевым словам
            if self.key_words_filter:
                if not any(keyword.lower() in (vac_obj.name.lower() + (vac_obj.requirement.lower() if vac_obj.requirement else '')) for keyword in self.key_words_filter):
                    continue

            # Добавление вакансии в список для отображения
            self.view_vacancy_objects_dict.append(vac_obj)

        # Вычисление максимального количества страниц
        self.max_page = math.ceil(len(self.view_vacancy_objects_dict) / self.results_on_page)

    def view_data(self):
        # Отображение данных с учетом пагинации
        while True:
            start_index = (self.current_page - 1) * self.results_on_page
            end_index = self.current_page * self.results_on_page

            # Проверка на пустой список вакансий
            if len(self.view_vacancy_objects_dict) == 0:
                print("Результаты не найдены.")
            for i in range(start_index, min(end_index, len(self.view_vacancy_objects_dict))):
                self.view_vacancy_objects_dict[i].display()

            # Ввод команды от пользователя
            current_command = 'r'
            while current_command not in self.commands_list:
                current_command = input('1 - Следующая страница   2 - Предыдущая страница   0 - Настройки\n')

            # Обработка команд
            if current_command == '1':
                self.switch_page(1)
            elif current_command == '2':
                self.switch_page(-1)
            elif current_command == '0':
                self.view_settings()

    def switch_page(self, increment):
        # Переключение страниц
        self.current_page += int(increment)
        if self.current_page < 1:
            self.current_page = 1
        elif self.current_page > self.max_page:
            self.current_page = self.max_page

    def view_settings(self):
        current_command = ""
        set_commands_list = ['1', '2', '3', '4', '5', '6', '0']
        while current_command != '0':
            while current_command not in set_commands_list:
                current_command = input('1 - Город   2 - Зарплата   3 - Ключевые слова   4 - Элементы на странице   5 - Новый запрос   6 - Топ N вакансий по зарплате   0 - Применить настройки\n')
            if current_command == '1':
                self.set_location_filter()
            elif current_command == '2':
                self.set_salary_filter()
            elif current_command == '3':
                self.set_keywords_filter()
            elif current_command == '4':
                self.set_results_on_page()
            elif current_command == '5':
                self.load_data()
            elif current_command == '6':
                n = int(input('Введите количество топ N вакансий по зарплате: '))
                top_vacancies = self.get_top_n_vacancies(n)
                for vacancy in top_vacancies:
                    vacancy.display()
            if current_command != '0':
                current_command = 'n'

        self.filter_view_data()


    def set_location_filter(self):
        # Установка фильтра по местоположению
        self.location_filter = input('Введите название города. (Оставьте пустое поле для всех.) \n')

    def set_salary_filter(self):
        # Установка фильтров по зарплате
        from_input = ""
        to_input = ""
        while not from_input.isdigit():
            from_input = input('Введите минимальную сумму зарплаты. (Оставьте пустое поле для всех.) \n')
            if from_input == "":
                break

        while not to_input.isdigit():
            to_input = input('Введите максимальную сумму зарплаты. (Оставьте пустое поле для всех.) \n')
            if to_input == "":
                break
        self.salary_from_filter = int(from_input) if from_input else None
        self.salary_to_filter = int(to_input) if to_input else None

    def set_keywords_filter(self):
        # Установка фильтров по ключевым словам
        self.key_words_filter = [keyword.strip().lower() for keyword in input('Введите ключевые слова для поиска через запятую. (Оставьте пустое поле для всех.) \n').split(',')]

    def set_results_on_page(self):
        # Установка количества результатов на странице
        results_on_page_input = ""
        while not results_on_page_input.isdigit():
            results_on_page_input = input('Введите количество результатов на странице. \n')
        self.results_on_page = int(results_on_page_input)
        self.max_page = math.ceil(len(self.view_vacancy_objects_dict) / self.results_on_page)

    def get_top_n_vacancies(self, n):
        sorted_vacancies = sorted(self.view_vacancy_objects_dict, key=lambda x: x.salary_from or 0, reverse=True)
        return sorted_vacancies[:n]
