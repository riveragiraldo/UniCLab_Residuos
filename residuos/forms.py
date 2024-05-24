from django import forms
from .models import *
from reactivos.forms import estandarizar_nombre
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Max, Min
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
    
 

# ------------------------------------ #
# Formulario para registro de residuos #
class EditResiduosForm(forms.ModelForm):
    # ficha_seguridad = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': ''}), required=False)
    
    def __init__(self, *args, **kwargs):
        # Extraer el valor máximo de solicitud del kwargs
        max_solicitud = kwargs.pop('max_solicitud', None)
        max_solicitud = REGISTRO_RESIDUOS.objects.filter(residuo_enviado=True).aggregate(Max('registro_solicitud'))['registro_solicitud__max']
        min_solicitud = REGISTRO_RESIDUOS.objects.filter(residuo_enviado=True).aggregate(Min('registro_solicitud'))['registro_solicitud__min']

        
        super(EditResiduosForm, self).__init__(*args, **kwargs)
        
        # Configurar el atributo max del campo registro_solicitud
        if max_solicitud is not None:
            self.fields['registro_solicitud'].widget.attrs.update({
                'min': min_solicitud,
                'step': '1',
                'max': max_solicitud
            })
        else:
            self.fields['registro_solicitud'].widget.attrs.update({
                'min': '1',
                'step': '1'
            })

    class Meta:
        model = REGISTRO_RESIDUOS
        fields = ['dependencia', 'area', 'laboratorio','nombre_residuo', 'cantidad', 'unidades', 'numero_envases', 'clasificado', 'estado', 'observaciones',  'registro_solicitud']
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
            'registro_solicitud': 'Número de Solicitud'
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
            'registro_solicitud': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1'})
            
        }
        # Obtener el máximo valor de registro_solicitud donde residuo_enviado=True en REGISTRO_RESIDUOS
        max_solicitud = REGISTRO_RESIDUOS.objects.filter(residuo_enviado=True).aggregate(Max('registro_solicitud'))['registro_solicitud__max']
        
    
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
    