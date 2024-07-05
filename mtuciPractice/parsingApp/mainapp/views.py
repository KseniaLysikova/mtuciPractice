from django.shortcuts import render, redirect
from .forms import ParsingForm, VacancyFilterForm
from django.utils.http import urlencode
from .models import Job
import requests
import json
import re


def home(request):
    if request.method == 'POST':
        form = ParsingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            salary = form.cleaned_data['salary']
            experience = form.cleaned_data['experience']
            area = form.cleaned_data['area']
            get_vacancies(name, salary, experience, area)

            return redirect('result')

    else:
        form = ParsingForm()
        return render(request, 'home.html', {'form': form})


def result(request):
    form = VacancyFilterForm(request.GET or None)
    vacancies = Job.objects.all()

    experience_choices = [
        ('noExperience', 'Нет опыта'),
        ('between1And3', 'От 1 года до 3 лет'),
        ('between3And6', 'От 3 до 6 лет'),
        ('moreThan6', 'Более 6 лет')
    ]

    if form.is_valid():
        name = form.cleaned_data.get('name', '')
        salary = form.cleaned_data.get('salary', 0)
        area = form.cleaned_data.get('area', '')
        experience = form.cleaned_data.get('experience', '')

        filters = {}
        if name:
            filters['name__icontains'] = name
        if salary:
            filters['salary__gte'] = salary
        if area:
            filters['area__icontains'] = area
        if experience:
            for choice in experience_choices:
                if experience == choice[0]:
                    filters['experience__icontains'] = choice[1]
                    break

        vacancies = vacancies.filter(**filters)

    total_vacancies = vacancies.count()

    context = {
        'form': form,
        'vacancies': vacancies,
        'total_vacancies': total_vacancies,
    }

    return render(request, 'result.html', context)


def get_vacancies(vacancy, salary, experience, area):
    url = 'https://api.hh.ru/vacancies'
    areas = get_areas()
    for i in range(len(areas)):
        if areas[i][3].lower() == area.lower():
            area = areas[i][2]
    params = {
        'text': vacancy,
        'area': area,
        'salary': salary,
        'experience': experience,
        'only_with_salary': True,
        'page': 1

    }

    response = requests.get(url, params=params)
    data = response.json()
    vacancies = []

    for item in data.get('items', []):
        name = item.get('name')

        if item.get('salary').get('from') is None:
            salary = int(item.get('salary').get('to'))
        elif item.get('salary').get('to') is None:
            salary = int(item.get('salary').get('from'))
        else:
            salary = int(item.get('salary').get('from'))

        if item.get('snippet') is None or item.get('snippet').get('responsibility') is None:
            description = None
        else:
            description = re.sub(r'<[^>]+>', '', item.get('snippet').get('responsibility'))

        if item.get('snippet') is None or item.get('snippet').get('requirement') is None:
            skills = None
        else:
            skills = re.sub(r'<[^>]+>', '', item.get('snippet').get('requirement'))

        experience = item.get('experience').get('name')
        work_format = item.get('employment').get('name') + ', ' + item.get('schedule').get('name')
        area = item.get('area').get('name')
        employer = item.get('employer').get('name')
        url = item.get('alternate_url')

        obj, created = Job.objects.update_or_create(
            url=url,
            defaults={
                'name': name,
                'salary': salary,
                'description': description,
                'skills': skills,
                'experience': experience,
                'work_format': work_format,
                'area': area,
                'employer': employer
            }
        )
        if created:
            vacancies.append(obj)
        for vacancy in vacancies:
            vacancy.save()


def get_areas():
    req = requests.get('https://api.hh.ru/areas')
    data = req.content.decode()
    req.close()
    js_obj = json.loads(data)
    areas = []
    for k in js_obj:
        for i in range(len(k['areas'])):
            if len(k['areas'][i]['areas']) != 0:
                for j in range(len(k['areas'][i]['areas'])):
                    areas.append([k['id'],
                                  k['name'],
                                  k['areas'][i]['areas'][j]['id'],
                                  k['areas'][i]['areas'][j]['name']])
            else:
                areas.append([k['id'],
                              k['name'],
                              k['areas'][i]['id'],
                              k['areas'][i]['name']])
    return areas
