from django import forms
from .models import UserProfile
from .models import Post
from django import template
from django_countries.widgets import CountrySelectWidget
register = template.Library()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'home_university', 'mobility_university', 'biography', 'profile_picture']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'hashtag_choice', 'custom_hashtag',
            'university', 'country', 'exchange_program', 'content'
        ]
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'form-select'}),
            'exchange_program': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'hashtag_choice':
                self.fields[field].widget.attrs.update({'class': 'form-select'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

