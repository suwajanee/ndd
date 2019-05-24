from django.conf.urls import url

from .views import agent_transport_add_view
from .views import agent_transport_delete_view
from .views import agent_transport_edit_view
from .views import agent_transport_page_view
from .views import agent_transport_data_view
from .views.agent_transport_print_view import AgentTransportPrintView


urlpatterns = [

    url(r'^$', agent_transport_page_view.agent_transport_page, name='agent-transport-page'),
    url(r'^add/$', agent_transport_add_view.agent_trnasport_add_page, name='agent-transport-add-page'),

    url(r'^api/get-agent-transports/$', agent_transport_page_view.api_get_agent_transports, name='api-get-agent-transports'),
    url(r'^api/filter-agent-transports/$', agent_transport_page_view.api_filter_agent_transports, name='api-filter-agent-transports'),

    url(r'^api/save-add-agent-transports/$', agent_transport_add_view.api_save_add_agent_transports, name='api-save-agent-transports'),
    url(r'^api/save-edit-agent-transports/$', agent_transport_edit_view.api_save_edit_agent_transport, name='api-save-edit-agent-transports'),
    url(r'^api/delete-agent-transports/$', agent_transport_delete_view.api_delete_agent_transports, name='api-delete-agent-transports'),

    url(r'^api/change-state-agent-transport/$', agent_transport_edit_view.api_change_state_agent_transport, name='api-change-state-agent-transport'),
    url(r'^api/change-color/$', agent_transport_edit_view.api_change_color_field, name='api-change-color-agent-trnasport'),

    url(r'^print/(?P<pk>\d+)/$', AgentTransportPrintView.as_view(), name='agent-transport-print'),

    # Summary
    url(r'^api/get-work-list/$', agent_transport_data_view.api_get_work_list, name='api-get-agent-transport-work-list'),


    url(r'^api/get-agent-transport-daily-works/$', agent_transport_data_view.api_get_agent_transport_daily_works, name='api-get-agent-transport-daily-works'),

    
]
