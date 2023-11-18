from django import forms
from .models import Topic, TopicComment


class TopicCommentForm(forms.ModelForm):
    class Meta:
        model = TopicComment
        fields = ['text']
        widgets = {
            'author': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
        }