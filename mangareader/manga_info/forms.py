from django import forms
from .models import Comment, CommentWorkMainPage


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'work': forms.HiddenInput(),
            'chapter': forms.HiddenInput(),
            'page': forms.HiddenInput(),
        }


class CommentWorkMainPageForm(forms.ModelForm):
    class Meta:
        model = CommentWorkMainPage
        fields = ['text']
        widgets = {
            'work': forms.HiddenInput()
        }
