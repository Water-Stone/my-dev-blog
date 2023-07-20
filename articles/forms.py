from django import forms
from .models import Article, Comment, HashTag

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'img']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': '3', 'cols':'35'})
        }


class HashTagForm(forms.ModelForm):
    class Meta:
        model = HashTag
        fields = ['name']