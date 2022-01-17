from django.urls import path

from . import views

app_name="music"
urlpatterns = [
    path('',views.index, name='index'),
    path('album/<album_id>/',views.album_view,name='album'),
    path('album/<album_id>/song/<song_id>/', views.song,name='song')
]
