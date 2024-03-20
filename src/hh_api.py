import requests


class HHApi:
    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def get_employer_vacancies(id_data):
        all_vacancies = []
        for i in id_data:
            url = f"https://api.hh.ru/vacancies?employer_id={i}"
            response = requests.get(url)

            vacancies_data = response.json().get("items", [])
            all_vacancies.extend(vacancies_data)

        return all_vacancies

    @staticmethod
    def get_employer_info(vacancy_data):
        data_list = []
        for vacancy in vacancy_data:
            employer_id = vacancy.get("employer", {}).get("id")
            employer_name = vacancy.get("employer", {}).get("name")
            employer_url = vacancy.get("employer", {}).get("alternate_url")
            vacancy_id = vacancy.get("id")
            vacancy_name = vacancy.get("name")
            salary_info = vacancy.get("salary", {})
            salary_from = salary_info.get("from") if salary_info else 0
            salary_to = salary_info.get("to") if salary_info else 0
            vacancy_url = vacancy.get("alternate_url")

            data_list.append({"employer_id": employer_id, "employer_name": employer_name, "employer_url": employer_url,
                              "vacancy_id": vacancy_id, "vacancy_name": vacancy_name, "salary_from": salary_from,
                              "salary_to": salary_to, "vacancy_url": vacancy_url})

        return data_list
