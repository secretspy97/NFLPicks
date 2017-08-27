from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mainPage, name='main'),
    url(r'^selectPicks/', views.getPicks, name='selectPicks'),
    url(r'^submitPicks/', views.submitPicks, name='submitPicks'),
    url(r'^results/', views.getResults, name='results'),
    url(r'^viewPicks/', views.getUserPicks, name='userPicks'),

]
