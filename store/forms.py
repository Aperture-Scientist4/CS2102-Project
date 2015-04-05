from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class SearchForm(forms.Form):
    @staticmethod
    def get_choices():
        return [('all', 'all'),('game','game'),('movie','movie'),('app','app'),('tv show','tv show')]
    def __init__(self,*args,**kwargs):
        super(SearchForm,self).__init__(*args,**kwargs)
        self.fields['keyword'] = forms.CharField(label='Keywords', required = False)
        self.fields['types'] = forms.ChoiceField(label='Categary',choices = SearchForm.get_choices())

class FeedbackForm(forms.Form):
    @staticmethod
    def get_choices():
        return [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]
    def __init__(self,*args,**kwargs):
        super(FeedbackForm,self).__init__(*args,**kwargs)
        self.fields['review'] = forms.CharField(label='Feedback', required = False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'placeholder': 'Review'}))
        self.fields['rating'] = forms.ChoiceField(label='Rating',widget=forms.RadioSelect, choices=FeedbackForm.get_choices())