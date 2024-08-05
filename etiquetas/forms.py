from django import forms
from .models import *


from .widgets import CustomClearableFileInput

class PictogramaForm(forms.ModelForm):
    class Meta:
        model = Pictograma
        fields = ['name', 'pictogram']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del pictograma',
                'title': 'El nombre debe tener un máximo de 50 caracteres.'
            }),
            'pictogram': CustomClearableFileInput(attrs={
                'class': 'form-control',
                'title': 'La imagen debe ser .png y tener dimensiones simétricas (igual ancho y altura).',
                'accept': '.png'
            }),
        }
        labels = {
            'name': 'Nombre',
            'pictogram': 'Pictograma',
        }

    def clean_pictogram(self):
        pictogram = self.cleaned_data.get('pictogram')
        
        # Validar la extensión
        if not pictogram.name.endswith('.png'):
            raise forms.ValidationError('El archivo debe tener la extensión .png.')
        
        # Validar el tamaño del archivo
        limit_kb = 100
        if pictogram.size > limit_kb * 1024:
            raise forms.ValidationError('El archivo no debe superar los 100 KB.')
        
        # Validar las dimensiones de la imagen
        from PIL import Image
        image = Image.open(pictogram)
        width, height = image.size
        if width != height:
            raise forms.ValidationError('La imagen debe ser simétrica (ancho y altura deben ser iguales).')
        
        return pictogram