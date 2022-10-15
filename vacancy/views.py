from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import BaseFormView, UpdateView

from .models import *
from .forms import UserApplicationForm, CompanyForm
from .mixins import OnlyUserWithoutCompanyMixin, OnlyUserWithCompanyMixin


class ListIndexView(ListView):
    template_name = 'index.html'
    model = Vacancy

    def get_context_data(self, *args, **kwargs):
        context = super(ListIndexView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        context['companies'] = Company.objects.all()
        return context


class ListVacanciesView(ListView):
    template_name = 'vacancy/vacancies.html'
    model = Vacancy

    def get_context_data(self, *args, **kwargs):
        context = super(ListVacanciesView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        return context


@method_decorator(login_required, name='post')
class DetailVacancyView(DetailView, BaseFormView):
    template_name = 'vacancy/vacancy.html'
    model = Vacancy
    form_class = UserApplicationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        application = form.save(commit=False)
        application.user = self.request.user
        application.vacancy_id = self.kwargs['pk']
        application.save()
        return super().form_valid(form)


class ListCategoryView(ListView):
    template_name = 'vacancy/vacancies_cat.html'
    model = Specialty
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_context_data(self, **kwargs):
        context = super(ListCategoryView, self).get_context_data(**kwargs)
        context['vacancy_list'] = Vacancy.objects.all()
        context['vacancy_title'] = Specialty.objects.filter(code=self.kwargs['code'])
        return context


class DetailCompanyView(DetailView):
    template_name = 'company/company.html'
    model = Company
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(DetailCompanyView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.filter(company_id=self.kwargs['id'])
        context['companies'] = Company.objects.all()
        return context


class MyCompanyLetsStart(OnlyUserWithoutCompanyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'company/company-create.html'


class MyCompanyBaseEditorView(LoginRequiredMixin, SuccessMessageMixin):
    model = Company
    template_name = 'company/company-edit.html'
    form_class = CompanyForm
    success_url = reverse_lazy('mycompany')


class MyCompanyCreateView(OnlyUserWithoutCompanyMixin, MyCompanyBaseEditorView, CreateView):
    success_message = 'Вы успешно создали компанию!'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MyCompanyEditView(OnlyUserWithCompanyMixin, MyCompanyBaseEditorView, UpdateView):
    success_message = 'Вы успешно обновили информацию о компании'

    def get_object(self, queryset=None):
        return self.request.user.company  # Возвращаем компанию пользователя


class MyVacancyList(OnlyUserWithCompanyMixin, ListView):
    model = Vacancy
    template_name = 'company/vacancy-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        company = self.request.user.company
        context = super(MyVacancyList, self).get_context_data(**kwargs)
        context['vacancies'] = company.vacancies.all().annotate(
            count=Count('applications'))  # Обращаемся ко всем вакансиям компании пользователя и считаем их
        return context


def tutut(request):
    return '404'
