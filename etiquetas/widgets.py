from django import forms

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'widgets/custom_clearable_file_input.html'
