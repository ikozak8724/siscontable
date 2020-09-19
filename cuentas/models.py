
from django.db import models
from django.db.models import Q

# Create your models here.


class Localidad(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300, default='')
    localidad = models.ForeignKey(
        Localidad, default=1, on_delete=models.PROTECT)
    email = models.EmailField()

    def __str__(self):
        return "{0}-{1} [{2}]".format(self.nombre, self.localidad, self.email)


class Movimiento(models.Model):
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    comprobante = models.TextField()
    fecha = models.DateField(auto_now=True)
    importe = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return "{}-{} - {}".format(self.fecha, self.cuenta.nombre, self.importe)

    @staticmethod
    def ultimos(idCuenta=None):
        if(idCuenta):
            return Movimiento.objects.filter(cuenta__id=idCuenta).order_by('-fecha')[0:3]
        else:
            return Movimiento.objects.order_by('-fecha')[0:3]

    @staticmethod
    def get_with(query, limit, start, end):
        q1 = Q(cuenta__nombre__contains=query)
        q2 = Q(comprobante__contains=query)
        q3 = Q(fecha__gte=start)
        q4 = Q(fecha__lte=end)

        queryset = Movimiento.objects.filter(q1 | q2)
        if start and end:
            queryset = Movimiento.objects.filter(q3 & q4)
        if limit:
            return queryset[:limit]
        return queryset


class PerfilEmpleado(models.Model):
    fecha_ingreso = models.DateField()
    sueldo = models.DecimalField(
        max_digits=20, decimal_places=2, default=20000)

    def __str__(self):
        return "{0}-{1}".format(self.fecha_ingreso, self.sueldo)


class GerenteDeCuentas(models.Model):
    nombre = models.CharField(max_length=300)
    cuentas = models.ManyToManyField(Cuenta)
    perfil = models.OneToOneField(
        PerfilEmpleado, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre