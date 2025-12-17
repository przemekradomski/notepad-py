from django import forms
import json
from .models import TitleNote, ContentNote, DataNote


class TitleNoteForm(forms.ModelForm):
    class Meta:
        model = TitleNote
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Wpisz tytuł notatki...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Wpisz treść notatki...'
            })
        }


class ContentNoteForm(forms.ModelForm):
    class Meta:
        model = ContentNote
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Wpisz treść notatki...'
            })
        }


class DataNoteForm(forms.ModelForm):
    data = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Wpisz dane JSON, np: {"klucz": "wartość"}'
        }),
        help_text='Wpisz dane w formacie JSON'
    )
    
    class Meta:
        model = DataNote
        fields = ['data']
    
    def clean_data(self):
        data_str = self.cleaned_data['data']
        try:
            # Spróbuj sparsować jako JSON
            if isinstance(data_str, str):
                data = json.loads(data_str)
                return data
            return data_str
        except json.JSONDecodeError:
            raise forms.ValidationError('Nieprawidłowy format JSON. Przykład: {"klucz": "wartość"}')

