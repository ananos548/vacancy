from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import BaseFormView, UpdateView

from vacancy.models import Vacancy, Specialty, Application, Company
from vacancy.forms import UserApplicationForm, VacancyForm
from vacancy.mixins import OnlyUserWithCompanyMixin


class MyVacancyBaseEditorView(LoginRequiredMixin, SuccessMessageMixin):
    model = Vacancy
    template_name = 'company/vacancy-edit.html'
    form_class = VacancyForm
    success_url = reverse_lazy('myvacancies_list')


class ListVacanciesView(ListView):
    template_name = 'vacancy/vacancies.html'
    model = Vacancy

    def get_context_data(self, *args, **kwargs):
        context = super(ListVacanciesView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all().only('title', 'skills', 'salary_min', 'salary_max',
                                                          'published_at')
        return context


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


class MyVacancyList(OnlyUserWithCompanyMixin, ListView):
    model = Vacancy
    template_name = 'company/vacancy-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        company = self.request.user.company
        context = super(MyVacancyList, self).get_context_data(**kwargs)
        context['vacancies'] = company.vacancies.all().annotate(
            count=Count('applications'))  # Обращаемся ко всем вакансиям компании пользователя и считаем их
        return context


class MyVacancyCreateView(OnlyUserWithCompanyMixin, MyVacancyBaseEditorView, CreateView, BaseFormView):

    def form_valid(self, form):
        form.instance.company = Company.objects.all().get(owner=self.request.user)
        return super().form_valid(form)


class MyVacancyEditView(OnlyUserWithCompanyMixin, MyVacancyBaseEditorView, UpdateView):

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(MyVacancyEditView, self).get_context_data()
        context['feedback'] = Application.objects.filter(vacancy_id=pk)
        return context

    def form_valid(self, form):
        pk = self.object.pk
        form.save()
        return redirect(reverse_lazy('myvacancy_edit', args=[pk]))
