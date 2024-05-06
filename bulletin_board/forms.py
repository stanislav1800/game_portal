from django import forms
from .models import Bulletin, Category, Response
from ckeditor.widgets import CKEditorWidget

class BulletinForm(forms.ModelForm):

    text = forms.CharField(widget=CKEditorWidget())
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={
            'required': 'Необходимо выбрать хотя бы одну категорию'
        }
    )

    class Meta:
        model = Bulletin
        fields = [
           'header',
           'text',
           'category',
       ]
        labels = {
            'header': 'Заголовок',
            'text': 'Текст',
            'category': 'Категория'
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text',)