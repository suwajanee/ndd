from django.urls import path
from django.conf.urls import url

from .views.agent_transport_add_view import AgentTransportAddView
from .views.agent_transport_delete_view import AgentTransportDeleteView
from .views.agent_transport_edit_view import AgentTransportEditTableView
from .views.agent_transport_print_view import AgentTransportPrintView
from .views.agent_transport_table_view import AgentTransportTableView


urlpatterns = [
    url(r'^$', AgentTransportTableView.render_table_agent_transport_page, name='agent-transport-table'),

    url(r'^print/(?P<pk>\d+)/$', AgentTransportPrintView.as_view(), name='agent-transport-print'),

    url(r'^add/$', AgentTransportAddView.render_add_agent_transport_page, name='agent-transport-add'),
    url(r'^save/$', AgentTransportAddView.save_data_agent_transport, name='agent-transport-save'), 

    url(r'^delete/(?P<pk>\d+)/$', AgentTransportDeleteView.delete_data_agent_transport, name='agent-transport-delete'), #delete in table page
    url(r'^delete/$', AgentTransportDeleteView.delete_multiple_data_agent_transport, name='agent-transport-delete-multiple'),

    url(r'^edit/$', AgentTransportEditTableView.render_edit_agent_transport_page, name='agent-transport-edit'),
    url(r'^edit/save$', AgentTransportEditTableView.save_edit_data_agent_transport, name='agent-transport-edit-save'),
]


