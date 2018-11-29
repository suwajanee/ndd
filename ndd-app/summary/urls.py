from django.conf.urls import url

from .views import summary_page_view


urlpatterns = [
    url(r'^$', summary_page_view.summary_page, name='summary-page'),

]
