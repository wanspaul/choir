from django.conf.urls import url
from attendance import views


urlpatterns = [
    url(r'^home/$', views.AttendanceHomeView.as_view(), name='home'),
    url(r'^add_practice/$', views.PracticeAddView.as_view(), name='add_practice'),
    url(r'^choir_list/(?P<practice_id>\d+)/(?P<part>\w+)$', views.ChoirListView.as_view(), name='choir_list'),
    url(r'^add_person/$', views.PersonAddView.as_view(), name='add_person'),
    url(r'^edit_person/(?P<person_id>\d+)$', views.PersonEditView.as_view(), name='edit_person'),
    url(r'^update_attendance/$', views.AttendanceEditView.as_view(), name='update_attendance'),

]
