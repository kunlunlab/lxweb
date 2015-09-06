from django.conf.urls import patterns, include, url
from filemanage import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^upload', views.upload_file, name='upload_file'),
    url('^list(\d{1})/(\d+)$', views.file_list, name='file_list'),
    url('^download(\d+)', views.download, name='download'),
)
