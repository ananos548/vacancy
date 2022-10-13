from django.contrib.auth.models import User
from django.db import models


class Specialty(models.Model):
    title = models.CharField(max_length=225)
    code = models.CharField(max_length=225)
    picture = models.ImageField(upload_to='MEDIA_SPECIALITY_IMAGE_DIR')

    def __str__(self):
        return f'{self.title}'


class Company(models.Model):
    name = models.CharField(max_length=225, verbose_name='Название Компании')
    location = models.CharField(max_length=225, verbose_name='География')
    logo = models.ImageField(upload_to='logo', verbose_name='Логотип')
    description = models.TextField(verbose_name='Информация о компании')
    employee_count = models.IntegerField(verbose_name='Количество работников')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='company')

    def __str__(self):
        return f'{self.name}'


class Vacancy(models.Model):
    title = models.CharField(max_length=225)
    skills = models.CharField(max_length=255)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')

    def __str__(self):
        return f'{self.title}'


class Application(models.Model):
    written_username = models.CharField(max_length=255, verbose_name='Имя')
    written_phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    written_cover_letter = models.TextField(verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
