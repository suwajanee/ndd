from django.conf.urls import url
from django.urls import path

from .views.booking_add_view import BookingAddView
from .views.booking_delete_view import BookingDeleteView
from .views.booking_edit_view import BookingEditTableView
from .views.booking_print_view import BookingPrintView
from .views.booking_table_view import BookingTableView
from .views.booking_time_view import BookingTimeView


urlpatterns = [
    url(r'^$', BookingTableView.render_table_booking_page, name='booking-table'),

    url(r'^add/$', BookingAddView.render_add_booking_page, name='booking-add'),
    url(r'^save/$', BookingAddView.save_data_booking, name='booking-save'), 

    url(r'^delete/(?P<pk>\d+)/$', BookingDeleteView.delete_data_booking, name='booking-delete'), #delete in table page
    url(r'^delete/$', BookingDeleteView.delete_multiple_data_booking, name='booking-delete-multiple'),

    url(r'^edit/$', BookingEditTableView.render_edit_booking_page, name='booking-edit'),
    url(r'^edit/save/$', BookingEditTableView.save_edit_data_booking, name='booking-edit-save'),

    # url(r'^print/(?P<pk>\d+)/(?P<template>\w+)/$', BookingPrintView.as_view(), name='booking-print'),
    url(r'^print/(?P<pk>\d+)/$', BookingPrintView.as_view(), name='booking-print'),

    url(r'^time/$', BookingTimeView.render_time_booking_page, name='booking-time'),
    url(r'^time/save/$', BookingTimeView.save_time_booking, name='booking-time-save'),

    url(r'^time/print/$', BookingPrintView.print_time, name='booking-print-time'),
]


