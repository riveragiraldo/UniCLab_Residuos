from django.db import models

# Create your models here.

from django.db import models

# --------------------- #
# Modelo de advertencia #
class Advertencia(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=30)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Advertencia"
        verbose_name_plural = "Advertencias"


# --------------- #
# Modelo Frases H #
class Frases_H(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=300)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Frase H"
        verbose_name_plural = "Frases H"

# --------------- #
# Modelo Frases P #
class Frases_P(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=300)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Frase P"
        verbose_name_plural = "Frases P"

# ----------------- #
# Modelo Pictograma #

class Pictograma(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    pictogram = models.ImageField(upload_to='pictogramas/', verbose_name="Pictograma")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Pictograma"
        verbose_name_plural = "Pictogramas"


# ----------------- #
# Modelo Sustancias #
class Sustancias(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=150)
    cas = models.CharField(verbose_name='CAS', max_length=40, blank=True, null=True)
    warning = models.ForeignKey(Advertencia, verbose_name='Advertencia', on_delete=models.SET_NULL, blank=True, null=True)
    phrase_h = models.ManyToManyField(Frases_H, verbose_name='Frases H', blank=True)
    phrase_p = models.ManyToManyField(Frases_P, verbose_name='Frases P', blank=True)
    pictogram_clp1 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 1', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp1')
    pictogram_clp2 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 2', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp2')
    pictogram_clp3 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 3', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp3')
    pictogram_clp4 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 4', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp4')
    pictogram_clp5 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 5', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp5')
    pictogram_clp6 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 6', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp6')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Sustancia"
        verbose_name_plural = "Sustancias"