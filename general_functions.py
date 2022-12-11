from terminaltables import AsciiTable


def predict_rub_salary(salary_from, salary_to):
    if not salary_from:
        predicted_salary = salary_to
        return predicted_salary
    if not salary_to:
        predicted_salary = salary_from
        return predicted_salary 
    else:    
        predicted_salary = (salary_to + salary_from)//2
        return predicted_salary


def create_table(input_descriptions, service_name):
    table_content = []
    table_headings = ["Язык программирования", "Найдено вакансий",
                      "Обработано вакансий", "Средняя зарплата"]
    table_content.append(table_headings)
    for language, content in input_descriptions.items():
        content = list(content.values())
        languages = [language]
        input_content = languages + content
        table_content.append(input_content)
    title = service_name
    table_instance = AsciiTable(table_content, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()
