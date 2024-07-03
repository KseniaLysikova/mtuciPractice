from django import forms
from .models import Job


class ParsingForm(forms.ModelForm):
    PLATFORM_CHOICES = [
        ('hh', 'hh.ru')
    ]
    EXPERIENCE_CHOICES = [
        ('noExperience', 'Нет опыта'),
        ('between1And3', 'От 1 года до 3 лет'),
        ('between3And6', 'От 3 до 6 лет'),
        ('moreThan6', 'Более 6 лет')
    ]
    platform = forms.ChoiceField(choices=PLATFORM_CHOICES)
    name = forms.CharField(required=True)
    salary = forms.IntegerField(required=True)
    experience = forms.ChoiceField(choices=EXPERIENCE_CHOICES)
    area = forms.CharField(required=True)

    class Meta:
        model = Job
        fields = ('name', 'salary', 'experience', 'area',)


class VacancyFilterForm(forms.ModelForm):
    EXPERIENCE_CHOICES = [
        ('noExperience', 'Нет опыта'),
        ('between1And3', 'От 1 года до 3 лет'),
        ('between3And6', 'От 3 до 6 лет'),
        ('moreThan6', 'Более 6 лет')
    ]
    experience = forms.ChoiceField(choices=EXPERIENCE_CHOICES)
    name = forms.CharField(required=True)
    salary = forms.IntegerField(required=False)
    area = forms.CharField(required=False)

    class Meta:
        model = Job
        fields = ('name', 'salary', 'experience', 'area')
