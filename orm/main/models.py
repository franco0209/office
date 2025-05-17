from django.db import models

class Empresa(models.Model):
    key = models.CharField(max_length=20, verbose_name="Clave única", unique=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre de la empresa")
    tipoTicket = models.CharField(max_length=10, verbose_name="Tipo de ticket")
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    key = models.CharField(max_length=20, verbose_name="Clave única", unique=True)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE, 
        verbose_name="Empresa",
        related_name='cuentas'  
    )
    nombre = models.CharField(max_length=255, verbose_name="Nombre de la cuenta")
    referencias = models.TextField(default='[]', null=True)
    
    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"
    
class Agencia(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre de la agencia")
    key = models.CharField(max_length=15, verbose_name="Nombre clave", unique= True)
    ciudad = models.CharField(max_length=20, verbose_name="Ciudad")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa", related_name="agencias")
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, verbose_name="Cuenta", related_name="Agencias")
    referencias = models.TextField(default='[]', null=True)

    
    class Meta:
        verbose_name = "Agencia"
        verbose_name_plural = "Agencias"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
class Inspector(models.Model):
    nombre = models.CharField(max_length=50, verbose_name= "Nombre completo", unique=True)
    nombreClave = models.CharField(max_length=20, verbose_name="Nombre clave")
    correo = models.CharField(max_length=20, verbose_name="Correo electrónico")
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, verbose_name="Empresa", related_name='inspectores', null=True)  
    cuentaDefault = models.OneToOneField(Cuenta, on_delete=models.SET_NULL, verbose_name="Cuenta",  null=True)
    isFemale = models.BooleanField(default= False, verbose_name="Sexo femenino")
    
    class Meta:
        verbose_name = "Inspector"
        verbose_name_plural = "Inspectores"
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombreClave
    
class Colaborador(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre Completo")
    dni = models.CharField(max_length=9, unique=True)
    tieneSCTR = models.BooleanField(default= True)
    
    def __str__(self):
        return self.nombre

class Cotizacion(models.Model):
    
    ESTADO_OPCIONES = [
        ('NUEVO', 'Nuevo'),
        ('EN_EJECUCION', 'En ejecución'),
        ('ATENDIDO', 'Atendido'),
    ]
    
    nombre = models.CharField(max_length=50)
    ppto = models.CharField(max_length=10, unique= True)
    agencia = models.ForeignKey(Agencia, on_delete=models.SET_NULL, verbose_name= "Agencia", null=True)
    inspector = models.ForeignKey(Inspector, on_delete=models.SET_NULL, verbose_name="Inspector",  null=True)
    codigoDelServicio = models.CharField(max_length=10, unique= True, default="SIN CODIGO")
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default="NUEVO", verbose_name="Estado de la cotización")
    costo = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.codigo}_{self.ppto}"
    
    
    
    
        