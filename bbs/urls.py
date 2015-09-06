from django.conf.urls import patterns, url, include

from bbs import views


urlpatterns = patterns('',

                       url('^list/(\d+)$', views.bbs_list, name='bbs_list'),
                       url(r'^detail/(\d+)/$', views.bbs_detail, name='bbs_detail'),
                       url(r'^sub_comment/$', views.sub_comment),
                       url(r'^bbs_pub/$', views.bbs_pub),
                       url(r'^bbs_sub/$', views.bbs_sub),

)

