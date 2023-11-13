from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'work': forms.HiddenInput(),
            'chapter': forms.HiddenInput(),
            'page': forms.HiddenInput(),
        }
