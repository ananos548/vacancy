from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import BaseFormView

from .models import *
from .forms import UserApplicationForm, CompanyForm


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





#@method_decorator(login_required, name='post')
# class LetStartView(TemplateView):
#     def get(self, request, pk):
#
#
#
#     def post(self, request, *args, **kwargs):
#         form = CompanyForm(request.POST, request.FILES)
#         if form.is_valid():
#             company = form.save(commit=False)
#             company.owner_id = request.user.id
#             company.save()
#             return redirect('/mycompany/')
#         return render(request, 'company/company-create.html', context={'form': form})
#
#
# @method_decorator(login_required, name='post')
# class MyCompanyEditView(DetailView):
#     success_url = '/mycompany'
#
#     def get(self, request, *args):
#         owner_id = request.user.id
#         company = Company.objects.filter(owner__id=owner_id)
#         if not company:
#             return redirect('/mycompany/letstart')
#         else:
#             form = CompanyForm()
#             return render(request, 'company/company-edit.html', context={'form': form})
#
#     def post(self, request, *args, **kwargs):
#         owner_id = request.user.id
#         company = Company.objects.filter(owner__id=owner_id)
#         form = CompanyForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/mycompany')
#         return render(request, 'company/company_edit.html', context={'form': form})


# class CompanyLetsStartView()