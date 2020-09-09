from django.db import models

# Create your models here.

class Localidad(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    nombre= models.CharField(max_length=200)
    direccion= models.CharField(max_length=300,default='')
    localidad= models.ForeignKey(Localidad,default=1, on_delete=models.PROTECT)
    email= models.EmailField()

    def __str__(self):
        return "{0}-{1} [{2}]".format(self.nombre,self.localidad,self.email)


class Movimiento(models.Model):
    cuenta= models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    comprobante= models.TextField()
    fecha= models.DateField(auto_now=True)
    importe =models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return  "{}-{} [{}]".format(self.cuenta.nombre,self.fecha,self.importe)
    
    @staticmethod
    def ultimos():
        return Movimiento.objects.order_by('-id')[:3]

class PerfilEmpleado(models.Model):
	fecha_ingreso = models.DateField()
	sueldo = models.DecimalField(max_digits=20, decimal_places=2, default=20000)

	def __str__(self):
		return "{0}-{1}".format(self.fecha_ingreso, self.sueldo)

class GerenteDeCuentas(models.Model):
	nombre = models.CharField(max_length = 300)
	cuentas = models.ManyToManyField(Cuenta)
	perfil = models.OneToOneField(PerfilEmpleado, null=True,on_delete=models.PROTECT)

	def __str__(self):
		return self.nombre
