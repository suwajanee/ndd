from django.conf.urls import url

from .views import employee_data_view
from .views import employee_page_view


urlpatterns = [

    url(r'^$', employee_page_view.employee_page, name='employee-page'),
    url(r'^officer/$', employee_page_view.employee_officer_page, name='employee-officer-page'),
    url(r'^driver/$', employee_page_view.employee_driver_page, name='employee-driver-page'),
    url(r'^mechanic/$', employee_page_view.employee_mechanic_page, name='employee-mechanic-page'),

    url(r'^api/get-employee/$', employee_data_view.api_get_employee, name='api-get-employee'),
    url(r'^api/get-employee-count/$', employee_data_view.api_get_employee_count, name='api-get-employee-count'),

]
