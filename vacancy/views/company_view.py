from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from vacancy.models import Vacancy, Company
from vacancy.forms import CompanyForm
from vacancy.mixins import OnlyUserWithoutCompanyMixin, OnlyUserWithCompanyMixin


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
