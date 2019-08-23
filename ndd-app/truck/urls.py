from django.conf.urls import url

from .views import truck_page_view


urlpatterns = [
    url(r'^$', truck_page_view.truck_page, name='truck-page'),
]
