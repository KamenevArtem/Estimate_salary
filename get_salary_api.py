import requests
import os
from general_functions import create_table
from general_functions import predict_rub_salary
from itertools import count
from dotenv import load_dotenv


def predict_rub_salary_hh(languages):
    url = "https://api.hh.ru/vacancies/"
    moscow_id = "1"
    dayly_coverage = "30"
    page_quantity = 20
    required_currency = "RUR"
    params = {
        "User-Agent": "api-test-agent",
        "text": "Программист",
        "area": {moscow_id},
        "period": {dayly_coverage},
        "only_with_salary": "True",
        "currency": "RUR",
        "page": "",
    }
    salary_description = {}
    for language in languages:
        params["text"] = language
        average_salary = 0
        vacancies_processed = 0
        for page_number in count(0, 1):
            params["page"] = page_number
            response = requests.get(url, params)
            response.raise_for_status()
            decoded_response = response.json()
            if page_number >= decoded_response["pages"] or page_number > page_quantity:
                break
            found_vacancies = decoded_response["found"]
            vacancies_description = decoded_response["items"]
            for vacancy in vacancies_description:
                salary_content = vacancy["salary"]
                salary_from = salary_content["from"]
                salary_to = salary_content["to"]
                currency = salary_content["currency"]
                if currency != required_currency:
                    continue
                predicted_salary = predict_rub_salary(salary_from, salary_to)
                vacancies_processed +=1   
                average_salary += predicted_salary
        if not vacancies_processed:
            average_salary = 0
            salary_description[language] = {
                "found_vacancies": found_vacancies,
                "vacancies_processed": "Нет вакансий с "
                "указанной зарплатой",
                "average_salary": "Нет вакансий с "
                "указанной зарплатой",
            }
        else:
            average_salary = average_salary//vacancies_processed
            salary_description[language] = {
                "found_vacancies": found_vacancies, 
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary,
            }
    return salary_description


def predict_rub_salary_sj(access_token, languages):
    url = "https://api.superjob.ru/2.0/vacancies/"
    moscow_id = "4"
    vacancies_per_page = "100"
    header = {
        "X-Api-App-Id": f"{access_token}",
    }
    params = {
        "town": {moscow_id},
        "keyword": "",
        "page": "",
        "count": {vacancies_per_page},
    }
    salary_description = {}
    for language in languages:
        params["keyword"] = language
        average_salary = 0
        vacancies_processed = 0
        for page_number in count(0,1):
            params["page"] = page_number
            response = requests.get(url, headers = header, params=params)
            response.raise_for_status()
            decoded_response = response.json()
            if page_number >= 5:
                break
            found_vacancies = decoded_response["total"]
            vacancie_description = decoded_response["objects"]
            for vacancie in vacancie_description:
                salary_from = vacancie["payment_from"]
                salary_to = vacancie["payment_to"]
                if not salary_from and not salary_to:
                    continue
                predicted_salary = predict_rub_salary(salary_from, salary_to)
                vacancies_processed += 1
                average_salary += predicted_salary
        if not vacancies_processed:
            average_salary = 0
            salary_description[language] = {
                "found_vacancies": found_vacancies,
                "vacancies_processed": "Нет вакансий с "
                "указанной зарплатой",
                "average_salary": "Нет вакансий с "
                "указанной зарплатой",
            }
        else:
            average_salary = average_salary//vacancies_processed
            salary_description[language] = {
                "found_vacancies": found_vacancies, 
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary,
            }
    return salary_description


def main():
    load_dotenv()
    access_token = os.environ["SUPERJOB_API_KEY"]
    languanges = ["C#", "Python", "C++", "Java Script",
                  "PHP", "Ruby", "go", "1c"]
    input_descriptions_sj = predict_rub_salary_sj(access_token, languanges)
    input_descriptions_hh = predict_rub_salary_hh(languanges)
    print(create_table(input_descriptions_sj, "SuperJob Moscow"))
    print(create_table(input_descriptions_hh, "HeadHunters Moscow"))


if __name__ == "__main__":
    main()
