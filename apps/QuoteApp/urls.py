from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^signup$', views.signup),
    url(r'^register$', views.regacc),
    url(r'^login$', views.logacc),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^addquote$', views.addquote),
    url(r'^user/(?P<id>[0-9]+)$', views.userpost),
    url(r'^editacc$', views.editacc),
    url(r'^editbt/(?P<id>[0-9]+)$', views.btedit),
    url(r'^postlike/(?P<id>[0-9]+)$', views.postlike),
    url(r'^delete/(?P<id>[0-9]+)$', views.delequote),
]