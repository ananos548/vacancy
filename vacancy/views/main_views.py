from django.db.models import Q
from django.views.generic import ListView
from vacancy.models import Vacancy, Specialty, Company


class ListIndexView(ListView):
    template_name = 'index.html'
    model = Vacancy

    def get_context_data(self, *args, **kwargs):
        context = super(ListIndexView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        context['companies'] = Company.objects.all()
        return context


class SearchView(ListView):
    model = Vacancy
    template_name = 'vacancy/vacancies.html'

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            vacancies = Vacancy.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) |
                                               Q(skills__icontains=query))
        else:
            vacancies = Vacancy.objects.all()
        return vacancies
