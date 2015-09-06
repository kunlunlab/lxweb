from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('base.urls', namespace='base')),

                       url(r'^$', 'base.views.login', name='login'),

                       url(r'^filemanage/', include('filemanage.urls', namespace='filemanage')),
                       url(r'^bbs/', include('bbs.urls', namespace='bbs')),
)

urlpatterns += staticfiles_urlpatterns()