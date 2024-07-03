import src.view_results

# Использование классов
# file_path = 'data/vacancies.json'
# file_worker = src.utils_hh.FileWorker(file_path)
# hh_parser = src.utils_hh.HH(file_worker)

# Загрузка вакансий по ключевому слову
# hh_parser.load_vacancies(input('Введите профессию для запроса\n'))

# Проверка содержимого файла
# with open(file_path, 'r', encoding='utf-8') as file:
#    saved_vacancies = json.load(file)
#    for vac in saved_vacancies:
#        if vac['snippet'] is not None:
#            print(vac['snippet']['requirement'])

src.view_results.ViewResults()
