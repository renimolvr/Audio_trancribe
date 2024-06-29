from django import forms
from .models import Recording

class RecordingForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional Title'}))

    class Meta:
        model = Recording
        fields = ('title',)
