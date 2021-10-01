from django import forms
from django.forms import widgets

from catalog.models import JobPost


class JobPostRequestForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title'})
    )
    description = forms.CharField(max_length=1000, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description'})
    )
    required_experience = forms.IntegerField(help_text="Years", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Required Experience'})
    )


    def clean_title(self):
        data = self.cleaned_data["title"]
        if len(data) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return data
    


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = '__all__'
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
        }