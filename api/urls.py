from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/(?P<user>\w+)/ps$', views.UserTaskView.as_view(), name='user_tasks'),
    url(r'^users$', views.UserView.as_view(), name='users'),
    url(r'ps/output/(?P<output>\w+)$', views.ProcessOutputView.as_view(), name='process_output'),
    url(r'ps/(?P<process>\w+)$', views.ProcessView.as_view(), name='process'),
    url(r'^ps$', views.PsView.as_view(), name='ps'),
]
