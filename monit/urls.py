from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'monit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^.*$', RedirectView.as_view(url='/admin/', permanent=True), name='index'),

]
