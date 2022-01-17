from django import forms

class ArtistForm(forms.Form):
    artist = forms.CharField(label='Search for an artist',max_length=50)
