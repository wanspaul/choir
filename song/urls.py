from django.conf.urls import url
from song import views


urlpatterns = [
    url(r'^home/$', views.SongHomeView.as_view(), name='home'),
    url(r'^add/$', views.SongAddView.as_view(), name='add'),
    url(r'^edit/(?P<song_no>\d+)$', views.SongEditView.as_view(), name='edit'),
]
