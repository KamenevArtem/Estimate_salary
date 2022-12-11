import requests
import os
from general_functions import create_table
from general_functions import predict_rub_salary
from itertools import count
from dotenv import load_dotenv


def predict_rub_salary_hh(languages):
    url = "https://api.hh.ru/vacancies/"
    params = {
        "User-Agent": "api-test-agent",
        "text": "Программист",
        "area": "1",
        "period": "30",
        "only_with_salary": "True",
        "currency": "RUR",
        "page": "",
    }
    salary_info = {}
    for language in languages:
        params["text"] = language
        average_salary = 0
        vacancies_processed = 0
        for page_number in count(0, 1):
            params["page"] = page_number
            response = requests.get(url, params)
            response.raise_for_status()
            response = response.json()
            if page_number >= response["pages"] or page_number > 20:
                break
            found_vacancies = response["found"]
            vacancies_description = response["items"]
            for vacancy in vacancies_description:
                salary_description = vacancy["salary"]
                salary_from = salary_description["from"]
                salary_to = salary_description["to"]
                currency = salary_description["currency"]
                if currency == "RUR":
                    predicted_salary = predict_rub_salary(salary_from, salary_to)
                    vacancies_processed +=1   
                    average_salary += predicted_salary
        average_salary = average_salary//vacancies_processed
        salary_info[language] = {
            "found_vacancies": found_vacancies, 
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary,
        }
    create_table(salary_info, "HeadHunters Moscow")


def predict_rub_salary_sj(access_token, languages):
    url = "https://api.superjob.ru/2.0/vacancies/"
    header = {
        "X-Api-App-Id": f"{access_token}",
    }
    params = {
        "town": "4",
        "keyword": "",
        "page": "",
        "count": "100",
    }
    vacancie_info = {}
    for language in languages:
        params["keyword"] = language
        average_salary = 0
        vacancies_processed = 0
        for page_number in count(0,1):
            params["page"] = page_number
            response = requests.get(url, headers = header, params=params)
            response.raise_for_status()
            response = response.json()
            if page_number >= 5:
                break
            found_vacancies = response["total"]
            vacancie_data = response["objects"]
            for vacancie in vacancie_data:
                salary_from = vacancie["payment_from"]
                salary_to = vacancie["payment_to"]
                if not salary_from and not salary_to:
                    continue
                else:
                    predicted_salary = predict_rub_salary(salary_from, salary_to)
                    vacancies_processed += 1
                    average_salary += predicted_salary
        if vacancies_processed == 0:
            average_salary = 0
        else:
            average_salary = average_salary//vacancies_processed
            vacancie_info[language] = {
                "found_vacancies": found_vacancies, 
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary,
            }
    create_table(vacancie_info, "SuperJob Moscow")


def main():
    load_dotenv()
    access_token = os.environ["SUPERJOB_API_KEY"]
    languanges = ["C#", "Python", "C++", "Java Script",
                  "PHP", "Ruby", "go", "1c"]
    predict_rub_salary_sj(access_token, languanges)
    predict_rub_salary_hh(languanges)


if __name__ == "__main__":
    main()
