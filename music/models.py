from django.db import models

# Create your models here.
class Artist(models.Model):
    artist_name=models.CharField(max_length=200)
    sp_id=models.CharField(max_length=200)

    def __str__(self):
        return self.artist_name

class Album(models.Model):
    artist=models.ForeignKey(Artist,on_delete=models.CASCADE)
    album_name=models.CharField(max_length=200)
    release_date=models.CharField(max_length=50)
    artwork=models.CharField(max_length=200)
    sp_id=models.CharField(max_length=200,default="_")

    def __str__(self):
        return self.album_name

class Song(models.Model):
    album=models.ForeignKey(Album,on_delete=models.CASCADE)
    song_name=models.CharField(max_length=50)
    duration=models.CharField(max_length=10,default='0:00')
    sp_id=models.CharField(max_length=200,default="_")
    def __str__(self):
        return self.song_name


