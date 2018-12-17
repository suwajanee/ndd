from django.conf.urls import url

from .views import summary_page_view
from .views import summary_year_view


urlpatterns = [
    url(r'^$', summary_page_view.summary_page, name='summary-page'),
    url(r'^form-setting/$', summary_page_view.summary_form_setting_page, name='summary-form-setting-page'),

    url(r'^api/get-summary-year/$', summary_year_view.api_get_summary_year, name='api-get-summary-year')

]
