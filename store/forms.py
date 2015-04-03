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
        return [('game','game'),('movie','movie'),('app','app'),('tv show','tv show')]
    def __init__(self,*args,**kwargs):
        super(SearchForm,self).__init__(*args,**kwargs)
        self.fields['keyword'] = forms.CharField(label='Keywords ', required = False)
        self.fields['types'] = forms.ChoiceField(label='Categary ',choices = SearchForm.get_choices())

class FeedbackForm(forms.Form):
    @staticmethod
    def get_choices():
        return [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]
    def __init__(self,*args,**kwargs):
        super(FeedbackForm,self).__init__(*args,**kwargs)
        self.fields['FeedbackBox'] = forms.CharField(label='Feedback ', required = False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10,}))
        self.fields['RatingBox'] = forms.ChoiceField(label='Rating ',choices = FeedbackForm.get_choices())

class RentForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(RentForm,self).__init__(*args,**kwargs)
        self.fields['DateBox'] = forms.DateField(label='ReturnDate ')

class AppEditForm(forms.Form):
    @staticmethod
    def get_Device():
        return [('1','1'),('2','2')]
    def __init__(self,*args,**kwargs):
        super(AppEditForm,self).__init__(*args,**kwargs)
        self.fields['AppName'] = forms.CharField(required=True)
        self.fields['RetailPrice'] = forms.DecimalField(required=True)
        self.fields['RentPrice'] = forms.DecimalField(required=False)
        self.fields['Genre'] = forms.ChoiceField(choices = FeedbackForm.get_choices())
        self.fields['ReleaseDate'] = forms.DateField(required=False)
        self.fields['Description'] = forms.CharField(required = False, widget=forms.Textarea(attrs={'cols': 60, 'rows':10,}))
