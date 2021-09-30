from django import forms


class DocumentForm(forms.Form):
    docfile = forms.ImageField(label='选择一个图片文件')
