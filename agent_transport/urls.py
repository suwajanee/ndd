from django.urls import path
from django.conf.urls import url
from .views.table_view import AgentTransportTableView
# from .views.print_view import BookingPrintView
# from .views.add_view import BookingAddView
# from .views.edit_table_view import BookingEditTableView
# from .views.authentication_view import AuthenticationView


urlpatterns = [
    url(r'^$', AgentTransportTableView.get_table, name='agent-transport-table'),
    # url(r'^print/(?P<pk>\d+)/(?P<template>\w+)/$', BookingPrintView.as_view(), name='booking-print'),

    # url(r'^add/$', BookingAddView.add_booking, name='booking-add'),
    # url(r'^save/$', BookingAddView.save_booking, name='booking-save'), 

    # url(r'^delete/(?P<pk>\d+)/$', BookingTableView.delete_data, name='booking-delete'), #delete in table page
    # url(r'^update/$', BookingTableView.update_data, name='booking-update'), #update in table page

    # url(r'^edit/$', BookingEditTableView.get_edit_table, name='booking-edit'),
    # url(r'^edit/save$', BookingEditTableView.save_edit_table, name='booking-edit-save'),
]


