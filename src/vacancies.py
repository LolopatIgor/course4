from src.utils import convert_salary


class VacancyObject:
    """
    Класс для представления вакансии.
    """

    def __init__(self, vacancy_dict):
        """
        Инициализирует объект VacancyObject на основе словаря с данными о вакансии.

        :param vacancy_dict: Словарь с данными о вакансии
        """
        # Инициализация атрибутов объекта
        self.requirement = None
        self.salary_from = None
        self.salary_to = None

        # Название вакансии
        self.name = vacancy_dict['name']

        # Локация (город) вакансии
        self.location = vacancy_dict['area']['name']

        # Проверка наличия информации о зарплате
        if vacancy_dict['salary'] is not None:
            # Конвертация и установка зарплаты "от" с использованием функции convert_salary
            self.salary_from = convert_salary(vacancy_dict['salary']['from'], vacancy_dict['salary']['currency'])
            # Конвертация и установка зарплаты "до" с использованием функции convert_salary
            self.salary_to = convert_salary(vacancy_dict['salary']['to'], vacancy_dict['salary']['currency'])

        # Проверка наличия информации о требованиях
        if vacancy_dict['snippet'] is not None:
            # Установка требований к вакансии
            self.requirement = vacancy_dict['snippet']['requirement']

    def __repr__(self):
        """
        Возвращает строковое представление объекта VacancyObject.

        :return: Строковое представление объекта
        """
        return (f"Vacancy: {self.name}\n"
                f"Location: {self.location}\n"
                f"Requirement: {self.requirement}\n"
                f"Salary from: {self.salary_from}\n"
                f"Salary to: {self.salary_to}\n")

    def display(self):
        """
        Выводит информацию о вакансии на экран.
        """
        # Вывод названия вакансии
        print(f"Название: {self.name}")

        # Вывод города вакансии
        print(f"Город: {self.location}")

        # Проверка наличия информации о зарплате и вывод её
        if self.salary_from or self.salary_to:
            print(f"Зарплата: {self.salary_from} - {self.salary_to} руб.")
        else:
            print("Зарплата: Не указана")

        # Проверка наличия требований и вывод их
        if self.requirement:
            print(f"Требования: {self.requirement}")
        else:
            print("Требования: Не указаны")

    # Методы сравнения
    def __lt__(self, other):
        return (self.salary_from or 0) < (other.salary_from or 0)

    def __le__(self, other):
        return (self.salary_from or 0) <= (other.salary_from or 0)

    def __gt__(self, other):
        return (self.salary_from or 0) > (other.salary_from or 0)

    def __ge__(self, other):
        return (self.salary_from or 0) >= (other.salary_from or 0)
