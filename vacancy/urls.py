from django.urls import path

from vacancy.views import vacancy_view, company_view, main_views

urlpatterns = [
    path('', main_views.ListIndexView.as_view(), name='index'),
    path('vacancies', vacancy_view.ListVacanciesView.as_view(), name='vacancy_list'),
    path('vacancies/cat/<str:code>', vacancy_view.ListCategoryView.as_view(), name='vacancies_cat'),
    path('companies/<int:id>', company_view.DetailCompanyView.as_view(), name='company'),
    path('vacancies/<int:pk>', vacancy_view.DetailVacancyView.as_view(), name='vacancy'),
    path('mycompany/letsstart', company_view.MyCompanyLetsStart.as_view(), name='letsstart'),
    path('mycompany/create/', company_view.MyCompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany/', company_view.MyCompanyEditView.as_view(), name='mycompany'),
    path('mycompany/vacancies/', vacancy_view.MyVacancyList.as_view(), name='myvacancies_list'),
    path('mycompany/vacancies/create/', vacancy_view.MyVacancyCreateView.as_view(), name='myvacancy_create'),
    path('mycompany/vacancies/<int:pk>', vacancy_view.MyVacancyEditView.as_view(), name='myvacancy_edit'),
    path('search', main_views.SearchView.as_view(), name='search'),
]
