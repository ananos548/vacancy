# https://github.com/albert-stepik-learn/stepik_vacancy1/blob/master/vacancy/data_import.py_
import os

import django
from vacancy.models import Vacancy, Company, Specialty
from vacancy import data


os.environ['DJANGO_SETTINGS_MODULE'] = 'stepik_vacancy1.settings'
django.setup()


for company_data in data.companies:
    Company.objects.create(
        id=company_data['id'],
        name=company_data['title'],
        logo=company_data['logo'],
        employee_count=company_data['employee_count'],
        location=company_data['location'],
        description=company_data['description'],
    )

for specialty_data in data.specialties:
    Specialty.objects.create(
        code=specialty_data['code'],
        title=specialty_data['title'],
    )

for vacancy_data in data.jobs:
    Vacancy.objects.create(
        id=vacancy_data['id'],
        title=vacancy_data['title'],
        specialty=Specialty.objects.get(code=vacancy_data['specialty']),
        company=Company.objects.get(id=vacancy_data['company']),
        salary_min=vacancy_data['salary_from'],
        salary_max=vacancy_data['salary_to'],
        published_at=vacancy_data['posted'],
        skills=vacancy_data['skills'],
        description=vacancy_data['description'],
    )

