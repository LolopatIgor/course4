import requests
import json
import os


class Parser:
    def __init__(self, file_worker):
        self.file_worker = file_worker

    def save_to_file(self, data):
        self.file_worker.save(data)


class FileWorker:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self, file_worker):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        super().__init__(file_worker)

    def load_vacancies(self, keyword):
        self.params['text'] = keyword
        self.params['page'] = 0
        while self.params['page'] < 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json().get('items', [])
            self.vacancies.extend(vacancies)
            self.params['page'] += 1

        self.save_to_file(self.vacancies)
