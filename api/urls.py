from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^person_detail/(?P<person_id>\d+)$', views.PersonDetailView.as_view(), name='person_detail'),
]
