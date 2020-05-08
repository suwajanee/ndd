from django.conf.urls import url

from .views import transport_report_add_view
from .views import transport_report_data_view
from .views import transport_report_delete_view
from .views import transport_report_edit_view
from .views import transport_report_page_view


urlpatterns = [

    url(r'^daily-expense/$', transport_report_page_view.daily_expense_page, name='daily-expense-page'),
    url(r'^daily-expense/(?P<date>\d[-\w]+)/(?P<co>[a-z]{3})', transport_report_page_view.date_expense_page, name='date-expense-page'),
    url(r'^daily-expense/(?P<date>\d[-\w]+)/(?P<driver>\d+)/$', transport_report_page_view.driver_expense_page, name='driver-expense-page'),

    url(r'^expense/(?P<year>\d+)/$', transport_report_page_view.yearly_expense_page, name='yearly-expense-page'),
    url(r'^total-expense/(?P<year>\d+)/$', transport_report_page_view.yearly_total_expense_page, name='yearly-total-expense-page'),

    url(r'^expense/$', transport_report_page_view.re_expense_page, name='re-expense-page'),
    url(r'^expense/(?P<year>\d+)/(?P<month>\d+)/(?P<co>[a-z]{3})/$', transport_report_page_view.expense_page, name='expense-page'),
    url(r'^expense/(?P<year>\d+)/(?P<month>\d+)/(?P<co>[a-z]{3})/(?P<period>[123]{1})/$', transport_report_page_view.period_expense_page, name='period-expense-page'),

    url(r'^total-expense/$', transport_report_page_view.re_total_expense_page, name='re-total-expense-page'),
    url(r'^total-expense/(?P<year>\d+)/(?P<month>\d+)/(?P<co>[a-z]{3})/$', transport_report_page_view.total_expense_page, name='total-expense-page'),
    url(r'^total-expense/(?P<year>\d+)/(?P<month>\d+)/(?P<co>[a-z]{3})/(?P<period>[123]{1})/$', transport_report_page_view.period_total_expense_page, name='period-total-expense-page'),


    url(r'^api/get-daily-expense/$', transport_report_data_view.api_get_daily_expense, name='api-get-daily-expense'),
    url(r'^api/get-daily-driver-expense/$', transport_report_data_view.api_get_daily_driver_expense, name='api-get-daily-driver-expense'),

    url(r'^api/get-expense-report/$', transport_report_data_view.api_get_expense_report, name='api-get-expense-report'),
    url(r'^api/filter-expense-report/$', transport_report_data_view.api_filter_expense_report, name='api-filter-expense-report'),

    url(r'^api/get-total-expense/$', transport_report_data_view.api_get_total_expense, name='api-get-total-expense'),

    # Add
    url(r'^api/add-expense-report/$', transport_report_add_view.api_add_expense_report, name='api-add-expense-report'),

    # Edit
    url(r'api/edit-expense-report/$', transport_report_edit_view.api_edit_expense_report, name='api-edit-expense-report'),

    # Delete
    url(r'api/delete-expense-report/$', transport_report_delete_view.api_delete_expense_report, name='api-delete-expense-report'),


]

