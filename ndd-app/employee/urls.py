from django.conf.urls import url

from .views import employee_data_view
from .views import employee_page_view
from .views import employee_add_view
from .views import employee_edit_view
from .views import employee_delete_view


urlpatterns = [

    url(r'^$', employee_page_view.employee_page, name='employee-page'),
    url(r'^officer/$', employee_page_view.employee_officer_page, name='employee-officer-page'),
    url(r'^driver/$', employee_page_view.employee_driver_page, name='employee-driver-page'),
    url(r'^mechanic/$', employee_page_view.employee_mechanic_page, name='employee-mechanic-page'),
    url(r'^not-active/$', employee_page_view.employee_not_active_page, name='employee-not-active-page'),
    url(r'^salary/$', employee_page_view.employee_salary_page, name='employee-salary-page'),

    url(r'^api/get-employee/$', employee_data_view.api_get_employee, name='api-get-employee'),
    url(r'^api/get-employee-count/$', employee_data_view.api_get_employee_count, name='api-get-employee-count'),

    url(r'^api/get-not-active-employee/$', employee_data_view.api_get_not_active_employee, name='api-get-not-active-employee'),

    url(r'^api/get-employee-salary/$', employee_data_view.api_get_employee_salary, name='api-get-employee-salary'),
    url(r'^api/get-salary-history/$', employee_data_view.api_get_salary_history, name='api-get-salary-history'),
    url(r'^api/edit-salary/$', employee_edit_view.api_edit_employee_salary, name='api-edit-salary'),
    
    url(r'^api/add-employee/$', employee_add_view.api_add_employee, name='api-add-employee'),

    url(r'^api/edit-employee/$', employee_edit_view.api_edit_employee, name='api-edit-employee'),
    url(r'^api/edit-pat-expired-driver/$', employee_edit_view.api_edit_pat_expired_driver, name='api-edit-pat-expired-driver'),

    url(r'^api/delete-employee/$', employee_delete_view.api_delete_employee, name='api-delete-employee'),


]