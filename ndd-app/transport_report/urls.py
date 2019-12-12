from django.conf.urls import url

from .views import transport_report_data_view
from .views import transport_report_page_view


urlpatterns = [

    url(r'^daily-expense/$', transport_report_page_view.daily_expense_page, name='daily-expense-page'),

    url(r'^daily-expense/(?P<date>\d[-\w]+)/(?P<co>[-\w]+)', transport_report_page_view.date_expense_page, name='date-expense-page'),


    url(r'^api/get-daily-expense/$', transport_report_data_view.api_get_daily_expense, name='api-get-daily-expense'),
    url(r'^api/get-by-summary-date/$', transport_report_data_view.api_get_by_summary_date, name='api-get-by-summary-date')

]

