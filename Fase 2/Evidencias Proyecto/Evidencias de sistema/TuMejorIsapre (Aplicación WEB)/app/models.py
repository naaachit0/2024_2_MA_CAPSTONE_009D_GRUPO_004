from django.db import models
from django.core.exceptions import ValidationError
import re

def validar_telefono_chileno(value):
    """Valida que el número de teléfono esté en formato chileno (+569XXXXXXXX o 9XXXXXXXX)"""
    if not re.match(r'^(?:\+569\d{8}|9\d{8})$', value):
        raise ValidationError('El número de teléfono debe estar en formato chileno (+569XXXXXXXX o 9XXXXXXXX).')
    
class Asesor(models.Model):
    asesor_id = models.CharField(max_length=10, unique=True, blank=True, null=True)  # ID único del asesor
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12, validators=[validar_telefono_chileno])

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        # Generar una ID única para el asesor si no existe
        if not self.asesor_id:
            self.asesor_id = f"ASE{self.pk or Asesor.objects.count() + 1:04d}"
        super().save(*args, **kwargs)


class Region(models.Model):
    reg_id = models.AutoField(primary_key=True)  
    reg_nombre = models.CharField(max_length=255) 

    def __str__(self):
        return self.reg_nombre

class Comunas(models.Model):
    com_id = models.AutoField(primary_key=True)
    com_nombre = models.CharField(max_length=255)
    region = models.ForeignKey(Region, related_name="comunas", on_delete=models.CASCADE, db_column="reg_id")

    def __str__(self):
        return f"{self.com_nombre} ({self.region.reg_nombre})"

class FormularioDatos(models.Model):
    nombre_apellido = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)
    fecha_nacimiento = models.DateField()
    renta_imponible = models.FloatField()
    num_cargas = models.IntegerField()
    telefono = models.CharField(max_length=12, validators=[validar_telefono_chileno])
    correo = models.EmailField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)  
    comuna = models.ForeignKey(Comunas, on_delete=models.SET_NULL, null=True) 
    prevision_actual = models.CharField(max_length=50)
    cambio_preferente = models.CharField(max_length=50)
    valor_uf = models.FloatField(default=0.0)
    resultado_final = models.IntegerField() 
    monto_dispuesto = models.IntegerField(null=True, blank=True)
    asesor = models.ForeignKey(Asesor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre_apellido

class Carga(models.Model):
    fecha_nacimiento = models.DateField()
    formulario = models.ForeignKey(FormularioDatos, related_name='cargas', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha_nacimiento)


