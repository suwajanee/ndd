from django.conf.urls import url

from .views import employee_page_view


urlpatterns = [

    url(r'^$', employee_page_view.employee_page, name='employee-page'),

]
