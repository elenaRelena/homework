from django.conf.urls import url
from . import views
from bookmaking.views import Registration
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.main_page),
    url(r'^user/$', views.user_view),
    url(r'^registration$', Registration.as_view()),
    url(r'^login$', views.log_in),
    url(r'^logout$', views.log_out),
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_detail, name="user_detail"),
    url(r'^user/(?P<pk>[0-9]+)/edit/$', views.edit_user),
    url(r'^horses/$', views.horses_list),
    url(r'^horse/(?P<pk>[0-9]+)/$', views.horse_detail, name="horse_detail"),
    url(r'^stake/$', views.make_stake, name="make_stake"),
    url(r'^stake/(?P<pk>\d+)/remove/$', views.stake_remove, name='stake_remove'),
    url(r'^rides/$', views.rides_list, name='rides_list'),
    url(r'^ride/(?P<pk>[0-9]+)/$', views.ride_detail, name='ride_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)