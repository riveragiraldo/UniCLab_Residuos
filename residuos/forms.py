from django import forms
from .models import *

class ClasificacionResiduosForm(forms.ModelForm):
    class Meta:
        model = CLASIFICACION_RESIDUOS
        fields = ['name', 'description']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción'
        }
        help_texts = {
            'name': 'Máximo 10 caracteres',
            'description': 'Máximo 500 caracteres'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'title':'El nombre de la clasificación debe ser de máximo 10 caracteres'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'title':'La descripción de la clasificación debe ser de máximo 500 caracteres','max':500})
        }
