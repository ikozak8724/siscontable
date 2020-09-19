from django.contrib import admin
from cuentas import models

# Register your models here.
class LocalidadAdmin(admin.ModelAdmin):
    ordering = ('nombre',)

class CuentaAdmin(admin.ModelAdmin):
    list_filter = ('localidad',)

class MovimientoAdmin(admin.ModelAdmin):
    date_hierarchy= 'fecha'
    list_filter = ('cuenta__nombre',)
    list_display = ('fecha', 'importe', 'cuenta')

admin.site.register(models.Localidad, LocalidadAdmin)
admin.site.register(models.Cuenta, CuentaAdmin)
admin.site.register(models.Movimiento, MovimientoAdmin)