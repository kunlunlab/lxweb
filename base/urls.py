from django.conf.urls import patterns, include, url
from base import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login$', views.login, name='login'),
    url(r'^home$', views.home, name='home'),
    url(r'^auth_code$', views.auth_code, name='auth_code'),

    url(r'^logout/$', views.logout_view),

)