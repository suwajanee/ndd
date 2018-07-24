from django.urls import path
from django.conf.urls import url
from .views.table_view import BookingTableView
from .views.print_view import BookingPrintView
from .views.add_view import BookingAddView


urlpatterns = [
    url(r'^$', BookingTableView.get_table, name='booking-table'),
    url(r'^print/(?P<pk>\d+)/(?P<template>\w+)/$', BookingPrintView.as_view(), name='booking-print'),
    url(r'^add/$', BookingAddView.add_booking, name='booking-add'),
    url(r'^save/$', BookingAddView.save_booking, name='booking-save'),

]


