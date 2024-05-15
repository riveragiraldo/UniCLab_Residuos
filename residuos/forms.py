from django import forms
from .models import *
from reactivos.forms import estandarizar_nombre
from django.core.exceptions import ValidationError

# ------------------------------------------- #
# Formulario para clasificaciones de residuos #
class ClasificacionResiduosForm(forms.ModelForm):
    def clean_name(self):
        # Obtener el valor del campo name
        name = self.cleaned_data['name']
        # Obtener la instancia actual (si existe)
        instance = getattr(self, 'instance', None)
        # Verificar si existe una clasificación con el mismo nombre (ignorando mayúsculas y minúsculas)
        if CLASIFICACION_RESIDUOS.objects.filter(name__iexact=name).exclude(pk=instance.pk).exists():
            raise forms.ValidationError("Ya existe una clasificación de residuos con este nombre.")
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        if 'description' in cleaned_data:
            cleaned_data['description'] = estandarizar_nombre(cleaned_data['description'])

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
            'name': forms.TextInput(attrs={'class': 'form-control', 'title': 'El nombre de la clasificación debe ser de máximo 10 caracteres'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'title': 'La descripción de la clasificación debe ser de máximo 500 caracteres', 'max': 500})
        }


# ------------------------------------ #
# Formulario para registro de residuos #
class RegistroResiduosForm(forms.ModelForm):
    # ficha_seguridad = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': ''}), required=False)
    
    def __init__(self, *args, **kwargs):
        super(RegistroResiduosForm, self).__init__(*args, **kwargs)
        self.fields['ficha_seguridad'] = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_ficha_seguridad', 'style': 'display: none;'}), required=False)
    
    class Meta:
        model = REGISTRO_RESIDUOS
        fields = ['dependencia', 'area', 'laboratorio','nombre_residuo', 'cantidad', 'unidades', 'numero_envases', 'clasificado', 'estado', 'observaciones' ]
        labels = {
            'dependencia': 'Tipo de Dependencia',
            'area': 'Área',
            'laboratorio': 'Laboratorio',
            'nombre_residuo': 'Nombre del Residuo',
            'cantidad': 'Cantidad',
            'unidades': 'Unidades',
            'numero_envases': 'Número de Envases',
            'clasificado': 'Clasificado',
            'estado': 'Estado',
            'observaciones':'Observaciones',
        }
        widgets = {
            'dependencia': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'laboratorio': forms.Select (attrs={'class': 'form-control'}),
            'nombre_residuo': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'unidades': forms.Select(attrs={'class': 'form-control'}),
            'numero_envases': forms.NumberInput(attrs={'class': 'form-control'}),
            'clasificado': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
    
    def clean(self):
        cleaned_data = super().clean()
        area = cleaned_data.get('area')
        nombre_residuo = cleaned_data.get('nombre_residuo')
        observaciones = cleaned_data.get('observaciones')

        if area is not None:
            cleaned_data['area'] = estandarizar_nombre(area)
        if nombre_residuo is not None:
            cleaned_data['nombre_residuo'] = estandarizar_nombre(nombre_residuo)
        if observaciones is not None:
            cleaned_data['observaciones'] = estandarizar_nombre(observaciones)

        return cleaned_data