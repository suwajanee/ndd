"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.generic import RedirectView

from booking.views import authentication_view
from booking.views import dashboard_view
from booking.views import export_xls_view
from booking.views.response_server import error_404, error_500
from summary.views import summary_page_view
from transport_report.views import expense_summary_date_view


urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),

    path('ndd-admin/', admin.site.urls),
    path('booking/', include('booking.urls')),
    path('agent-transport/', include('agent_transport.urls')),
    path('customer/', include('customer.urls')),
    path('summary/', include('summary.urls')),
    path('employee/', include('employee.urls')),
    path('truck-chassis/', include('truck.urls')),
    path('report/', include('transport_report.urls')),

    url(r'^dashboard/$', dashboard_view.dashboard_page, name='dashboard-page'),
    url(r'^staff/$', authentication_view.login, name='login'),
    url(r'^logout/$', authentication_view.logout, name='logout'),

    url(r'^$', RedirectView.as_view(url='/staff/')),

    url(r'^export/$', export_xls_view.export_page, name='export-page'),
    url(r'^export/excel/$', export_xls_view.export_xls, name='export-excel'),

    url(r'^cheque/$', summary_page_view.cheque_page, name='cheque-page'),

    # Data
    url(r'^api/get-weekly-works/$', dashboard_view.api_get_weekly_works, name='api-get-weekly-works'),
    url(r'^api/get-yearly-income/$', dashboard_view.api_get_income, name='api-get-yearly-income'),

    # Expense Summary Date
    url(r'^summary-date/(?P<year>\d+)/$', expense_summary_date_view.summary_date_page, name='summary-date-page'),
    url(r'^summary-date/api/get-summary-date/$', expense_summary_date_view.api_get_summary_date, name='api-get-summary-date'),
    url(r'^summary-date/api/add-summary-date/$', expense_summary_date_view.api_add_summary_date, name='api-add-summary-date'),
    url(r'^summary-date/api/edit-summary-date/$', expense_summary_date_view.api_edit_summary_date, name='api-edit-summary-date'),
    url(r'^summary-date/api/delete-summary-date/$', expense_summary_date_view.api_delete_summary_date, name='api-delete-summary-date'),

]


handler404 = error_404
handler500 = error_500


