from django.contrib import admin

# Register your models here.
from .models import *
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# ------------------------------------------------------- #
# Resource para la importación para el modelo Advertencia #
class AdvertenciaResources(resources.ModelResource):
    class Meta:
        model = Advertencia


# -------------------------------------------- #
# Inclusión del modelo Advertencia en el Admin #
@admin.register(Advertencia)
class Advertenciaadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('name',)
    list_per_page=10
    ordering=('id',)
    resource_class = AdvertenciaResources


# ------------------------------------------------------- #
# Resource para la importación para el modelo Frases h #
class FrasesHResources(resources.ModelResource):
    class Meta:
        model = Frases_H

# ----------------------------------------- #
# Inclusión del modelo Frases H en el Admin #
@admin.register(Frases_H)
class FrasesHadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('name',)
    list_per_page=10
    ordering=('id',)
    resource_class = FrasesHResources



# ------------------------------------------------------- #
# Resource para la importación para el modelo Frases p #
class FrasesPResources(resources.ModelResource):
    class Meta:
        model = Frases_P

# ----------------------------------------- #
# Inclusión del modelo Frases H en el Admin #
@admin.register(Frases_P)
class FrasesPadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('name',)
    list_per_page=10
    ordering=('id',)
    resource_class = FrasesPResources



# ------------------------------------------------------- #
# Resource para la importación para el modelo Pictogramas #
class PictogramasResources(resources.ModelResource):
    class Meta:
        model = Pictograma

# -------------------------------------------- #
# Inclusión del modelo Pictogramas en el Admin #
@admin.register(Pictograma)
class Pictogramaadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', )
    list_per_page = 10
    ordering = ('id',)
    resource_class = PictogramasResources

    def pictogram_image(self, obj):
        if obj.pictogram:
            return format_html(
                '<a href="{}" download><img src="{}" width="50" height="50" /></a>',
                obj.pictogram.url,
                obj.pictogram.url
            )
        return "-"
    pictogram_image.short_description = 'Pictogram'


# ------------------------------------------------------ #
# Resource para la importación para el modelo Sustancias #
class SustanciasResources(resources.ModelResource):
    class Meta:
        model = Sustancias

# ------------------------------------------- #
# Inclusión del modelo Sustancias en el Admin #
@admin.register(Sustancias)
class Sustanciasadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'id','name', 'cas', 'warning', 'phrase_h_list', 'phrase_p_list','pictogram_clp1_thumbnail', 
        'pictogram_clp2_thumbnail', 'pictogram_clp3_thumbnail', 
        'pictogram_clp4_thumbnail', 'pictogram_clp5_thumbnail', 
        'pictogram_clp6_thumbnail'
    )
    list_per_page = 500
    ordering = ('id',)
    resource_class = SustanciasResources

    # Organiza Frases H alfabéticamente
    def phrase_h_list(self, obj):
        phrases = obj.phrase_h.all().order_by('name')
        return mark_safe('<br>'.join([str(phrase) for phrase in phrases]))

    phrase_h_list.short_description = 'Frase H'

    # Organiza Frases P alfabéticamente
    def phrase_p_list(self, obj):
        phrases = obj.phrase_p.all().order_by('name')
        return mark_safe('<br>'.join([str(phrase) for phrase in phrases]))

    phrase_p_list.short_description = 'Frase P'

    # Miniatura para Pictograma CLP1
    def pictogram_clp1_thumbnail(self, obj):
        return self._thumbnail(obj.pictogram_clp1)

    pictogram_clp1_thumbnail.short_description = 'Pictograma CLP 1'
    pictogram_clp1_thumbnail.allow_tags = True

    # Miniatura para Pictograma CLP2
    def pictogram_clp2_thumbnail(self, obj):
        return self._thumbnail(obj.pictogram_clp2)

    pictogram_clp2_thumbnail.short_description = 'Pictograma CLP 2'
    pictogram_clp2_thumbnail.allow_tags = True

    # Miniatura para Pictograma CLP3
    def pictogram_clp3_thumbnail(self, obj):
        return self._thumbnail(obj.pictogram_clp3)

    pictogram_clp3_thumbnail.short_description = 'Pictograma CLP 3'
    pictogram_clp3_thumbnail.allow_tags = True

    # Miniatura para Pictograma CLP4
    def pictogram_clp4_thumbnail(self, obj):
        return self._thumbnail(obj.pictogram_clp4)

    pictogram_clp4_thumbnail.short_description = 'Pictograma CLP 4'
    pictogram_clp4_thumbnail.allow_tags = True

    # Miniatura para Pictograma CLP5
    def pictogram_clp5_thumbnail(self, obj):
        return self._thumbnail(obj.pictogram_clp5)

    pictogram_clp5_thumbnail.short_description = 'Pictograma CLP 5'
    pictogram_clp5_thumbnail.allow_tags = True

    # Miniatura para Pictograma CLP6
    def pictogram_clp6_thumbnail(self, obj):
        return self._thumbnail(obj.pictogram_clp6)

    pictogram_clp6_thumbnail.short_description = 'Pictograma CLP 6'
    pictogram_clp6_thumbnail.allow_tags = True

    # Método auxiliar para generar la miniatura y el enlace de descarga
    def _thumbnail(self, pictogram):
        if pictogram and pictogram.pictogram:
            return mark_safe(
                f'<a href="{pictogram.pictogram.url}" download>'
                f'<img src="{pictogram.pictogram.url}" width="50" height="50" />'
                f'</a>'
            )
        return ""

    # Mostrar miniaturas en las filas del admin
    _thumbnail.short_description = 'Miniatura'
