import os

def load_employer_ids(file_path):
    with open(file_path, 'r') as file:
        employer_ids = [line.strip() for line in file]
    return employer_ids

# # Определение относительного пути к файлу
# relative_path = os.path.join('employers_id.txt')
#
# # Получение абсолютного пути к файлу
# file_path = os.path.join(relative_path)
#
# # Загрузка идентификаторов работодателей из файла
# print(load_employer_ids(relative_path))