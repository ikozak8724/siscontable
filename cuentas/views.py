import datetime
from django.shortcuts import render
from django.http import HttpResponse, Http404
from cuentas.models import Cuenta
from cuentas.models import Movimiento 

# Create your views here.

def hoy(reqest):
    ahora= datetime.datetime.now()
    html= '<html><body><h1>{0}.<h1/></body></html>'.format(ahora)
    return HttpResponse(html)

def cuentas(reqest):
    cuentas= Cuenta.objects.all()
    total= Cuenta.objects.all().count()
    return render(reqest,
        'cuentas2.html',
        {'cuentas':cuentas,
        'total':total})
    
def cuenta(request,id):
	try:
		cuenta= Cuenta.objects.get(pk=id)
	except Cuenta.DoesNotExist:
		raise Http404("La cuenta no existe")

	return render(request,
			'cuenta.html', 
			{'cuenta':cuenta, 'movimientos': Movimiento.ultimos()})