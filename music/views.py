from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from .forms import ArtistForm
apikey = "2fc874c09d9a7b8a3fa4357678400342"
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid="05e4e928a80e4c3abca5cd0f9c62815c"
sid="b6556d42453a4898938db1cef5eeb6a6"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=sid)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
from .models import Artist, Album, Song

def ms_to_min(millis):
    millis = int(millis)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    return f'{minutes}:{seconds}'



def index(request):
    error = ''
    albums = []
    new_artist = Artist()
    if request.method=='POST':
        form = ArtistForm(request.POST)

        if form.is_valid():
            artist=form.cleaned_data['artist']

            exists = Artist.objects.filter(artist_name=artist).count()
            if exists > 0:
                artist_obj = Artist.objects.get(artist_name=artist)
                albums = artist_obj.album_set.all()
            else:
                r = sp.search(q=f"artist:{artist}",type='album',market='US',limit=50)
                if 'error' in r:
                    print('Couldn\'t find results for this artist! Please try again')
                    error = 'Couldn\'t find results for this artist! Please try again'
                else:
                    albums = r['albums']['items']
                    new_artist = Artist(artist_name=artist,sp_id=albums[0]['artists'][0]['id'])
                    new_artist.save()

                    for album in albums:
                        album_id=album['id']
                        image=album['images'][0]['url']

                        new_album = new_artist.album_set.create(artist=artist, album_name=album['name'],release_date=album['release_date'],artwork=image,sp_id=album_id)

                    albums=new_artist.album_set.all()

    else:
        form=ArtistForm()

    return render(request, 'music/index.html', {'form':form,'albums': albums, 'error':error})




def album_view(request,album_id):
    album = Album.objects.get(sp_id=album_id)
    artwork = album.artwork

    exists = album.song_set.all().count()
    if exists > 0:
        song_set = album.song_set.all()
    else:
        tracks = sp.album_tracks(album_id, limit=50, offset=0, market='US')
        songs = tracks['items']

        for s in songs:
            s['duration_ms'] = ms_to_min(s['duration_ms'])
            album.song_set.create(song_name=s['name'],duration=(s['duration_ms']),sp_id=s['id'])

        song_set = album.song_set.all()

    return render(request, 'music/album.html',{'songs': song_set,'artwork':artwork,'album_name': album.album_name})


def song(request,album_id,song_id):
    song_obj = Song.objects.get(sp_id=song_id)
    track = sp.track(song_id,market="US")
    print(track['preview_url'])
    album = Album.objects.get(sp_id=album_id)

    return render(request, 'music/song.html',{'preview':track['preview_url'],'album':album,'song_name':song_obj.song_name})