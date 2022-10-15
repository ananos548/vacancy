from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', ListIndexView.as_view(), name='index'),
    path('vacancies', ListVacanciesView.as_view(), name='vacancy_list'),
    path('vacancies/cat/<str:code>', ListCategoryView.as_view(), name='vacancies_cat'),
    path('companies/<int:id>', DetailCompanyView.as_view(), name='company'),
    path('vacancies/<int:pk>', DetailVacancyView.as_view(), name='vacancy'),
    path('mycompany/letsstart', MyCompanyLetsStart.as_view(), name='letsstart'),
    path('mycompany/create/', MyCompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany/', MyCompanyEditView.as_view(), name='mycompany'),
    path('mycompany/vacancies/', MyVacancyList.as_view(), name='mycompany_vacancies'),
    # path('mycompany/vacancies/create/'),
    # path('mycompany/vacancies/<int:vacancy_id>', mycompany_vacancies_detail),
]
