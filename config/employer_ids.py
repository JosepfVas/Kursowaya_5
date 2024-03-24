def load_employer_ids(file_path):
    """ Функция для получения данных из файла. """
    with open(file_path, 'r') as file:
        employer_ids = [line.strip() for line in file]
    return employer_ids
