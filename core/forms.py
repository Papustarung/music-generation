from django import forms
from .models import Creator, Library, Song, GenerationJob


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField()
    display_name = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        pw2 = cleaned_data.get('password_confirm')
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


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
