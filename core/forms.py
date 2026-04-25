from django import forms
from .models import Creator, Library, Song, GenerationJob
from .models.enum import Genre, VocalStyle, Occasion


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
    """FR-18: Creator can only toggle visibility of their song."""
    class Meta:
        model = Song
        fields = ['visibility']


class GenerationJobForm(forms.ModelForm):
    class Meta:
        model = GenerationJob
        fields = ['creator', 'song', 'status', 'title', 'story', 'genre', 'vocal_style', 'occasion', 'lyrics']
        widgets = {
            'story': forms.Textarea(attrs={'rows': 4}),
            'lyrics': forms.Textarea(attrs={'rows': 4}),
        }


CONTENT_RULES = [
    'No violent, threatening, or harmful content.',
    'No hate speech, discrimination, or slurs targeting any group.',
    'No explicit sexual content.',
    'No content that harasses or targets a specific real person.',
    'No promotion of illegal activities or substances.',
    'No copyright-infringing lyrics reproduced verbatim.',
]

BLOCKED_KEYWORDS = [
    'kill', 'murder', 'rape', 'terrorist', 'bomb', 'suicide',
    'genocide', 'nazi', 'child porn', 'molest', 'torture',
]


class GenerateSongForm(forms.Form):
    """
    User-facing form for FR-06 / FR-07 / FR-34 / FR-35.
    Only exposes input fields — creator, status, and song are set by GenerationService.
    """
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. My Birthday Song'}),
    )
    story = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe what the song should be about…'}),
        help_text='Tell the story or mood you want the song to convey.',
    )
    genre = forms.ChoiceField(choices=Genre.choices)
    vocal_style = forms.ChoiceField(choices=VocalStyle.choices)
    occasion = forms.ChoiceField(choices=Occasion.choices)
    lyrics = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional — add phrases or ideas to inspire the lyrics, e.g. "freedom, open road, chasing dreams"'}),
        help_text='Leave blank to let the AI write the lyrics freely, or add phrases to guide them.',
    )
    content_rules_accepted = forms.BooleanField(
        label='I have read and agree to the content rules.',
        error_messages={'required': 'You must accept the content rules before generating.'},
    )

    def clean(self):
        cleaned_data = super().clean()
        fields_to_check = [
            cleaned_data.get('title', ''),
            cleaned_data.get('story', ''),
            cleaned_data.get('lyrics', ''),
        ]
        combined = ' '.join(fields_to_check).lower()
        for keyword in BLOCKED_KEYWORDS:
            if keyword in combined:
                raise forms.ValidationError(
                    'Your request contains content that violates our content rules and cannot be processed.'
                )
        return cleaned_data

