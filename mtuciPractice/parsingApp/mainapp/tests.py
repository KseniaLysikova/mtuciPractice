from django.test import TestCase, Client
from django.urls import reverse
from .models import Job


class VacancyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.vacancy_data = {
            'name': 'test_job',
            'salary': 25000,
            'description': 'test description',
            'skills': 'test skills',
            'experience': 'Нет опыта',
            'work_format': 'test format',
            'area': 'Химки',
            'employer': 'test employer',
            'url': 'https://hh.ru/vacancy/11111',
        }
        self.vacancy = Job.objects.create(**self.vacancy_data)

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vacancy Search')

    def test_filter_vacancy(self):
        response = self.client.get('/result/', {'name': 'test_job', 'experience': 'Нет опыта'})
        self.assertEqual(response.context['vacancies'].count(), 1)
        self.assertEqual(response.context['vacancies'][0].name, 'test_job')
        self.assertEqual(response.context['vacancies'][0].experience, 'Нет опыта')

        response = self.client.get('/result/', {'salary': 25000, 'experience': 'Нет опыта'})
        self.assertEqual(response.context['vacancies'].count(), 1)
        self.assertEqual(response.context['vacancies'][0].salary, 25000)

        response = self.client.get('/result/', {'area': 'Химки', 'experience': 'Нет опыта'})
        self.assertEqual(response.context['vacancies'][0].area, 'Химки')

    def test_update_data(self):
        duplicate_job = self.vacancy_data
        duplicate_job['area'] = 'Some area'
        obj, created = Job.objects.update_or_create(duplicate_job)
        if created:
            obj.save()
        self.assertEqual(Job.objects.get(name='test_job').area, 'Some area')
