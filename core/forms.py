from django import forms
from .models import Creator, Library, Song, GenerationJob


class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['email', 'display_name', 'token_amount']


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['creator']


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['library', 'title', 'story', 'genre', 'vocal_style', 'occasion', 'visibility', 'lyrics', 'audio_location']
        widgets = {
            'story': forms.Textarea(attrs={'rows': 4}),
            'lyrics': forms.Textarea(attrs={'rows': 4}),
        }


class GenerationJobForm(forms.ModelForm):
    class Meta:
        model = GenerationJob
        fields = ['creator', 'song', 'status', 'title', 'story', 'genre', 'vocal_style', 'occasion', 'lyrics']
        widgets = {
            'story': forms.Textarea(attrs={'rows': 4}),
            'lyrics': forms.Textarea(attrs={'rows': 4}),
        }
