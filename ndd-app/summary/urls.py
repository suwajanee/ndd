from django.conf.urls import url

from .views import cheque_data_view
from .views import commission_view
from .views import summary_apll_invoice
from .views import summary_chart_data
from .views import summary_customer_custom_view
from .views import summary_customer_view
from .views import summary_form_setting_view
from .views import summary_invoice_details_view
from .views import summary_invoice_view
from .views import summary_month_view
from .views import summary_page_view
from .views import summary_week_view
from .views import summary_year_view

from .views import summary_damco_invoice
from .views import summary_oocl_invoice
from .views import summary_report_export
from .views.summary_print_view import SummaryPrintView, SummaryEvergreenPrintView


urlpatterns = [
    url(r'^$', summary_page_view.summary_page, name='summary-page'),
    url(r'^form-setting/$', summary_page_view.summary_form_setting_page, name='summary-form-setting-page'),
    url(r'^customer-custom/$', summary_page_view.summary_customer_custom_page, name='summary-customer-custom-page'),
    url(r'^chart/(?P<year>\d+)/$', summary_page_view.summary_chart_page, name='summary-chart-page'),

    url(r'^(?P<year>\d+)/$', summary_page_view.summary_year_details_page, name='summary-year-details-page'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', summary_page_view.summary_month_details_page, name='summary-month-details-page'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<week>\d+)/$', summary_page_view.summary_week_details_page, name='summary-week-details-page'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<week>\d+)/(?P<customer>\w+)/$', summary_page_view.summary_invoice_page, name='summary-invoice-page'),

    url(r'^commission/$', summary_page_view.commission_page, name='summary-commission-page'),


    # Summary Year
    url(r'^api/add-year/$', summary_year_view.api_add_year, name='api-add-year'),
    url(r'^api/get-year/$', summary_year_view.api_get_year, name='api-get-year'),
    url(r'^api/get-summary-year/$', summary_year_view.api_get_summary_year, name='api-get-summary-year'),

    url(r'^api/get-summary-year-details/$', summary_year_view.api_get_summary_year_details, name='api-get-summary-year-details'),

    # Form Setting
    url(r'^api/get-form-default/$', summary_form_setting_view.api_get_form_default, name='api-get-form-default'),
    url(r'^api/get-form/$', summary_form_setting_view.api_get_summary_form, name='api-get-form'),
    url(r'^api/add-form/$', summary_form_setting_view.api_add_summary_form, name='api-add-form'),
    url(r'^api/edit-form/$', summary_form_setting_view.api_edit_summary_form, name='api-edit-form'),
    url(r'^api/delete-form/$', summary_form_setting_view.api_delete_summary_form, name='api-delete-form'),

    # Customer Custom
    url(r'^api/get-customer-custom/$', summary_customer_custom_view.api_get_customer_custom, name='api-get-customer-custom'),
    url(r'^api/add-customer-custom/$', summary_customer_custom_view.api_add_customer_custom, name='api-add-customer-custom'),
    url(r'^api/edit-customer-custom/$', summary_customer_custom_view.api_edit_customer_custom, name='api-edit-customer-custom'),
    # url(r'^api/delete-customer-custom/$', summary_customer_custom_view.api_delete_customer_custom, name='api-delete-customer-custom'),

    # Summary Month
    url(r'^api/get-summary-month-details/$', summary_month_view.api_get_summary_month_details, name='api-get-summary-month-details'),
    
    # Summary Week
    url(r'^api/check-week-exist/$', summary_week_view.api_check_week_exist, name='api-check-week-exist'), #Check week
    url(r'^api/get-summary-week-details/$', summary_week_view.api_get_summary_week_details, name='api-get-summary-week-details'),
    url(r'^api/add-summary-week/$', summary_week_view.api_add_summary_week, name='api-add-summary-week'),
    url(r'^api/edit-summary-week/$', summary_week_view.api_edit_summary_week, name='api-edit-summary-week'),
    url(r'^api/get-summary-weeks-by-year/$', summary_week_view.api_get_summary_weeks_by_year, name='api-get-summary-weeks-by-year'),
    url(r'^api/get-summary-weeks-by-month/$', summary_week_view.api_get_summary_weeks_by_month, name='api-get-summary-weeks-by-month'),
    url(r'^api/summary-weeks-status/$', summary_week_view.api_summary_week_status, name='api-summary-weeks-status'),

    # Summary Customer
    url(r'^api/edit-summary-customer-detail/$', summary_customer_view.api_edit_summary_customer_detail, name='api-edit-summary-customer-detail'),
    url(r'^api/summary-customer-status/$', summary_customer_view.api_summary_customer_status, name='api-summary-customer-status'),

    # Invoice
    url(r'^api/get-invoice/$', summary_invoice_view.api_get_invoice, name='api-get-invoice'),
    url(r'^api/edit-invoice-remark/$', summary_invoice_view.api_edit_invoice_remark, name='api-edit-invoice-remark'),
    url(r'^api/invoice-status/$', summary_invoice_view.api_invoice_status, name='api-invoice-status'),
    url(r'^api/add-invoice/$', summary_invoice_view.api_add_invoice, name='api-add-invoice'),
    url(r'^api/edit-invoice-week/$', summary_invoice_view.api_edit_invoice_week, name='api-edit-invoice-week'),
    url(r'^api/delete-invoice-week/$', summary_invoice_view.api_delete_invoice_week, name='api-delete-invoice-week'),

    url(r'^api/copy-invoice/$', summary_invoice_view.api_copy_invoice, name='api-copy-invoice'),

    # Invoice Details
    url(r'^api/get-invoice-details/$', summary_invoice_details_view.api_get_invoice_details, name='api-get-invoice-details'),
    url(r'^api/add-invoice-details/$', summary_invoice_details_view.api_add_invoice_details, name='api-add-invoice-details'),
    url(r'^api/delete-invoice-detail/$', summary_invoice_details_view.api_delete_invoice_detail, name='api-delete-invoice-detail'),
    url(r'^api/edit-invoice-details/$', summary_invoice_details_view.api_edit_invoice_details, name='api-edit-invoice-details'),
    url(r'^api/check-container/$', summary_invoice_details_view.api_check_container, name='api-check-container'),

    # Evergreen
    url(r'^api/add-invoice-details-evergreen/$', summary_invoice_details_view.api_add_invoice_details_evergreen, name='api-add-invoice-details-evergreen'),


    # Print
    url(r'^print/(?P<pk>\d+)/$', SummaryPrintView.as_view(), name='summary-print'),
    url(r'^print-evergreen/(?P<pk>\d+)/$', SummaryEvergreenPrintView.as_view(), name='summary-evergreen-print'),

    # Export
    url(r'^export/report/$', summary_report_export.report_export, name='summary-report'),
    url(r'^export/oocl-invoice/$', summary_oocl_invoice.oocl_invoice, name='summary-oocl-invoice'),
    url(r'^export/damco-invoice/$', summary_damco_invoice.damco_invoice, name='summary-damco-invoice'),

    # Beautiful Soup
    url(r'^export/apll-invoice/$', summary_apll_invoice.apll_invoice, name='summary-apll-invoice'),

    # Chart
    url(r'^api/get-summary-year-data/$', summary_chart_data.api_summary_year_total_chart, name='api-get-summary-year-data'),
    url(r'^api/get-summary-customer-data/$', summary_chart_data.api_summary_customer_total_chart, name='api-get-summary-customer-data'),

    # Cheque
    url(r'^api/get-cheque-data/$', cheque_data_view.api_get_cheque_data, name='api-get-cheque-data'),
    url(r'^api/edit-cheque-accept-date/$', cheque_data_view.api_edit_cheque_accept_date, name='api-edit-cheque-accept-date'),

    # Commission
    url(r'^api/get-commission-data/$', commission_view.api_get_commission_data, name='api-get-commission-data'),

]
