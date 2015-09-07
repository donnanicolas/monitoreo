from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'ps', views.PsView.as_view(), name='ps'),
    url(r'^users/(?P<user>\w+)/tasks$', views.UserTaskView.as_view(), name='user_tasks'),
    url(r'users', views.UserView.as_view(), name='users'),
]
