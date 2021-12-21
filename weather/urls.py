from django.urls import path

from . import views
api_key =  "f072269bbbc8eb8f7be71129bbd95c0d"
app_name = 'weather'
urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<city_name>/',views.delete_city,name='delete_city')
]