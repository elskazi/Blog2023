from django import forms
from .models import Comment

# форма дял отправки писем их не надо нигде сохранять, forms.Form
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

# форма для коментанирев, сохраняется в БД, forms.ModelForm
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

# Поиск
class SearchForm(forms.Form):
    query = forms.CharField()