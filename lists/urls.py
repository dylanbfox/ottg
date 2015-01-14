from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^(\d+)/add_item$', 'lists.views.add_item', name='view_list'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),
)
