import requests
import json
import os


class Parser:
    def __init__(self, file_worker):
        """
        Базовый класс для парсеров. Инициализирует объект FileWorker для работы с файлами.

        :param file_worker: Объект для работы с файлами
        """
        self.file_worker = file_worker

    def save_to_file(self, data):
        """
        Сохраняет данные в файл с использованием объекта FileWorker.

        :param data: Данные для сохранения
        """
        self.file_worker.save(data)


class FileWorker:
    def __init__(self, file_path):
        """
        Класс для работы с файлами. Инициализирует путь к файлу.

        :param file_path: Путь к файлу
        """
        self.file_path = file_path

    def save(self, data):
        """
        Сохраняет данные в файл в формате JSON.

        :param data: Данные для сохранения
        """
        # Создание директорий, если их нет
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # Открытие файла для записи и сохранение данных в формате JSON
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        # Метод для загрузки данных из файла

    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

        # Метод для удаления файла

    def delete(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


class HH(Parser):
    """
    Класс для работы с API HeadHunter. Наследует базовый класс Parser.
    """

    def __init__(self, file_worker):
        """
        Инициализация объекта HH, установка начальных значений.

        :param file_worker: Объект для работы с файлами
        """
        # URL для API HeadHunter
        self.url = 'https://api.hh.ru/vacancies'

        # Заголовки для запроса
        self.headers = {'User-Agent': 'HH-User-Agent'}

        # Параметры запроса
        self.params = {'text': '', 'page': 0, 'per_page': 100}

        # Список для хранения вакансий
        self.vacancies = []

        # Вызов инициализатора родительского класса
        super().__init__(file_worker)

    def load_vacancies(self, keyword):
        """
        Загружает вакансии с API HeadHunter по заданному ключевому слову и сохраняет их в файл.

        :param keyword: Ключевое слово для поиска вакансий
        """
        # Установка ключевого слова для поиска
        self.params['text'] = keyword

        # Сброс номера страницы на 0
        self.params['page'] = 0

        # Цикл для загрузки данных с нескольких страниц
        while self.params['page'] < 20:
            # Отправка GET запроса к API HeadHunter
            response = requests.get(self.url, headers=self.headers, params=self.params)

            # Получение списка вакансий из ответа
            vacancies = response.json().get('items', [])

            # Добавление вакансий в общий список
            self.vacancies.extend(vacancies)

            # Увеличение номера страницы для следующего запроса
            self.params['page'] += 1

        # Сохранение всех загруженных вакансий в файл
        self.save_to_file(self.vacancies)
