# forms.py
from django import forms
from .models import Annotation

class UploadFileForm(forms.Form):
    file = forms.FileField()


class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ['title_id', 'annotate']
        widgets = {
            'annotate': forms.Select(choices=Annotation.ANNOTATE_CHOICES),   
        }

# class TextSelectionForm(forms.ModelForm):
#     class Meta:
#         model = SelectedText 
#         fields = ['title_id','selected_text']