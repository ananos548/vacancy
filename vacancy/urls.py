from django.urls import path

from vacancy.views.vacancy_view import ListVacanciesView, MyVacancyEditView, MyVacancyCreateView, DetailVacancyView, \
    MyVacancyList, ListCategoryView
from vacancy.views.company_view import MyCompanyCreateView, MyCompanyLetsStart, DetailCompanyView, MyCompanyEditView
from vacancy.views.main_views import ListIndexView, SearchView

urlpatterns = [
    path('', ListIndexView.as_view(), name='index'),
    path('vacancies', ListVacanciesView.as_view(), name='vacancy_list'),
    path('vacancies/cat/<str:code>', ListCategoryView.as_view(), name='vacancies_cat'),
    path('companies/<int:id>', DetailCompanyView.as_view(), name='company'),
    path('vacancies/<int:pk>', DetailVacancyView.as_view(), name='vacancy'),
    path('mycompany/letsstart', MyCompanyLetsStart.as_view(), name='letsstart'),
    path('mycompany/create/', MyCompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany/', MyCompanyEditView.as_view(), name='mycompany'),
    path('mycompany/vacancies/', MyVacancyList.as_view(), name='myvacancies_list'),
    path('mycompany/vacancies/create/', MyVacancyCreateView.as_view(), name='myvacancy_create'),
    path('mycompany/vacancies/<int:pk>', MyVacancyEditView.as_view(), name='myvacancy_edit'),
    path('search', SearchView.as_view(), name='search'),
]
