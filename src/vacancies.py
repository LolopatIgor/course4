from src.utils import convert_salary


class VacancyObject:

    def __init__(self, vacancy_dict):
        self.requirement = None
        self.salary_from = None
        self.salary_to = None
        self.name = vacancy_dict['name']
        self.location = vacancy_dict['area']['name']
        if vacancy_dict['salary'] is not None:
            self.salary_from = convert_salary(vacancy_dict['salary']['from'], vacancy_dict['salary']['currency'])
            self.salary_to = convert_salary(vacancy_dict['salary']['to'], vacancy_dict['salary']['currency'])
        if vacancy_dict['snippet'] is not None:
            self.requirement = vacancy_dict['snippet']['requirement']

    def display(self):
        print(f"Название: {self.name}")
        print(f"Город: {self.location}")
        if self.salary_from or self.salary_to:
            print(f"Зарплата: {self.salary_from} - {self.salary_to} руб.")
        else:
            print("Зарплата: Не указана")
        if self.requirement:
            print(f"Требования: {self.requirement}")
        else:
            print("Требования: Не указаны")