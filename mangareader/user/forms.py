from django import forms
from .models import CustomUser
from manga_info.models import Author, Chapter, Work


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'subscribers']


class ChangeAuthorForm(forms.ModelForm):
    old_name = forms.CharField(max_length=100)
    old_last = forms.CharField(max_length=100)

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'subscribers']

    field_order = ['old_name', 'old_last', 'first_name', 'last_name', 'subscribers']


class DeleteAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']


class AddChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'chapter', 'work', 'image']

    def __init__(self, *args, **kwargs):
        super(AddChapterForm, self).__init__(*args, **kwargs)
        self.fields['work'] = forms.ModelChoiceField(queryset=Work.objects.all())


class ChangeChapterForm(forms.ModelForm):
    old_title = forms.CharField(max_length=100)
    old_work = forms.ModelChoiceField(queryset=Work.objects.all())

    class Meta:
        model = Chapter
        fields = ['title', 'chapter', 'work', 'image']

    def __init__(self, *args, **kwargs):
        super(ChangeChapterForm, self).__init__(*args, **kwargs)
        self.fields['work'] = forms.ModelChoiceField(queryset=Work.objects.all())

    field_order = ['old_title', 'old_work', 'title', 'chapter', 'work', 'image']
