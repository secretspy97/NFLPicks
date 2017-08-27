from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^createUser/', views.createUser, name='createUser'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^profile/', views.profile, name='profile'),

]
