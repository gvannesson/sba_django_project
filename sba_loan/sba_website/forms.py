from django import forms 
from .models import News


class CreateNews(forms.ModelForm):
    
    class Meta:
        model = News
        fields = ['items','date_news','content','news_url']
        widgets = {'date_news': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'})}

