from django.db import models

class FormularioDatos(models.Model):
    nombre_apellido = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)
    fecha_nacimiento = models.DateField()
    renta_imponible = models.FloatField()
    num_cargas = models.IntegerField()
    telefono = models.CharField(max_length=9)
    correo = models.EmailField()
    region = models.CharField(max_length=255)
    comuna = models.CharField(max_length=255)
    prevision_actual = models.CharField(max_length=50)
    cambio_preferente = models.CharField(max_length=50)
    valor_uf = models.FloatField(default=0.0)
    resultado_final = models.IntegerField() 
    monto_dispuesto = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre_apellido

class Carga(models.Model):
    fecha_nacimiento = models.DateField()
    formulario = models.ForeignKey(FormularioDatos, related_name='cargas', on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha_nacimiento
    

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

