from django.conf.urls import url

from .views import employee_data_view
from .views import employee_page_view
from .views import employee_add_view
from .views import employee_edit_view
from .views import employee_delete_view


urlpatterns = [

    url(r'^$', employee_page_view.employee_page, name='employee-page'),
    url(r'^:(?P<job>\w+)$', employee_page_view.employee_job_page, name='employee-job-page'),
    url(r'^former/$', employee_page_view.former_employee_page, name='former-employee-page'),
    url(r'^salary/$', employee_page_view.employee_salary_page, name='employee-salary-page'),

    # Get
    url(r'^api/get-job/$', employee_data_view.api_get_job, name='api-get-job'),
    url(r'^api/get-employee/$', employee_data_view.api_get_employee, name='api-get-employee'),
    url(r'^api/get-former-employee/$', employee_data_view.api_get_former_employee, name='api-get-former-employee'),
    url(r'^api/get-employee-salary/$', employee_data_view.api_get_employee_salary, name='api-get-employee-salary'),
    # Add
    url(r'^api/add-employee/$', employee_add_view.api_add_employee, name='api-add-employee'),
    # Edit
    url(r'^api/edit-employee/$', employee_edit_view.api_edit_employee, name='api-edit-employee'),
    url(r'^api/edit-pat-expired-driver/$', employee_edit_view.api_edit_pat_expired_driver, name='api-edit-pat-expired-driver'),

    # Salary
    url(r'^api/get-salary-history/$', employee_data_view.api_get_salary_history, name='api-get-salary-history'),
    url(r'^api/edit-salary/$', employee_edit_view.api_edit_employee_salary, name='api-edit-salary'),
    url(r'^api/delete-latest-salary/$', employee_delete_view.api_delete_latest_salary, name='api-delete-latest-salary'),
    
]
