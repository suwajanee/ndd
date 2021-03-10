from django.conf.urls import url

from .views import transport_report_add_view
from .views import transport_report_data_view
from .views import transport_report_delete_view
from .views import transport_report_edit_view
from .views import transport_report_page_view


urlpatterns = [
    # Daily - Driver
    url(r'^daily-report/$', transport_report_page_view.re_daily_report_page, name='re-daily-report-page'),
    url(r'^daily-report/(?P<date>\d[-\w]+)/$', transport_report_page_view.daily_report_page, name='daily-report-page'),
    url(r'^daily-report/(?P<date>\d[-\w]+)/(?P<driver>\d+)/$', transport_report_page_view.driver_report_page, name='driver-report-page'),
    # Yearly
    url(r'^expense/(?P<year>\d+)/$', transport_report_page_view.yearly_expense_page, name='yearly-expense-page'),
    url(r'^summary/(?P<year>\d+)/$', transport_report_page_view.yearly_summary_page, name='yearly-summary-page'),
    url(r'^total-expense/(?P<year>\d+)/$', transport_report_page_view.yearly_total_expense_page, name='yearly-total-expense-page'),
    # Expense Report
    url(r'^expense/$', transport_report_page_view.re_expense_page, name='re-expense-page'),
    url(r'^expense/(?P<year>\d+)/(?P<month>\d+)/$', transport_report_page_view.expense_page, name='expense-page'),
    url(r'^expense/(?P<year>\d+)/(?P<month>\d+)/(?P<period>[123]{1})/$', transport_report_page_view.period_expense_page, name='period-expense-page'),
    # Summary
    url(r'^summary/$', transport_report_page_view.re_summary_page, name='re-summary-page'),
    url(r'^summary/(?P<year>\d+)/(?P<month>\d+)/$', transport_report_page_view.report_summary_page, name='report-summary-page'),
    url(r'^summary/(?P<year>\d+)/(?P<month>\d+)/(?P<period>[123]{1})/$', transport_report_page_view.period_summary_page, name='period-summary-page'),
    # Total Expense
    url(r'^total-expense/$', transport_report_page_view.re_total_expense_page, name='re-total-expense-page'),
    url(r'^total-expense/(?P<year>\d+)/(?P<month>\d+)/$', transport_report_page_view.total_expense_page, name='total-expense-page'),
    url(r'^total-expense/(?P<year>\d+)/(?P<month>\d+)/(?P<period>[123]{1})/$', transport_report_page_view.period_total_expense_page, name='period-total-expense-page'),
    # Total Truck
    url(r'^total-truck/$', transport_report_page_view.re_total_truck_page, name='re-total-truck-page'),
    url(r'^total-truck/(?P<year>\d+)/(?P<month>\d+)/$', transport_report_page_view.total_truck_page, name='total-truck-page'),

    # Get
    url(r'^api/get-daily-report/$', transport_report_data_view.api_get_daily_report, name='api-get-daily-report'),
    url(r'^api/get-default-driver-truck/$', transport_report_data_view.api_get_default_driver_truck, name='api-get-default-driver-truck'),

    url(r'^api/get-expense-report/$', transport_report_data_view.api_get_expense_report, name='api-get-expense-report'),
    url(r'^api/filter-expense-report/$', transport_report_data_view.api_filter_expense_report, name='api-filter-expense-report'),
    url(r'^api/get-expense-report-by-id-list', transport_report_data_view.api_get_expense_report_by_id_list, name='api-get-expense-report-by-id-list'),

    url(r'^api/get-total-expense/$', transport_report_data_view.api_get_total_expense, name='api-get-total-expense'),

    url(r'^api/get-total-truck/$', transport_report_data_view.api_get_total_truck, name='api-get-total-truck'),

    url(r'^api/get-used-order-type-by-work-id/$', transport_report_data_view.api_get_used_order_type_by_work_id, name='api-get-used-order-type-by-work-id'),

    # Add
    url(r'^api/add-expense-report/$', transport_report_add_view.api_add_expense_report, name='api-add-expense-report'),

    # Edit
    url(r'api/edit-expense-report/$', transport_report_edit_view.api_edit_expense_report, name='api-edit-expense-report'),
    url(r'api/edit-price-list/$', transport_report_edit_view.api_edit_price_list, name='api-edit-price-list'),

    # Delete
    url(r'api/delete-expense-report/$', transport_report_delete_view.api_delete_expense_report, name='api-delete-expense-report'),


]

