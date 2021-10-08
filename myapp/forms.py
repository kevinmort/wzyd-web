from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    docfile = forms.ImageField(label='选择一个图片文件')
    class Meta:
        model = Document
        fields = '__all__'
