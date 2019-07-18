from django.conf.urls import url

from .views import employee_page_view


urlpatterns = [

    url(r'^$', employee_page_view.employee_page, name='employee-page'),
    url(r'^api/get-employee/$', employee_page_view.api_get_employee, name='api-get-employee'),

]
