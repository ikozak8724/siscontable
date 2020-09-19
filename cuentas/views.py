from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse, Http404
from cuentas.models import Cuenta, Movimiento
from cuentas.forms import SearchForm, MovimientoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)


def cuentas(request):
    cuentas = Cuenta.objects.all()
    total = Cuenta.objects.all().count()
    return render(request, 'cuentas2.html', {'cuentas': cuentas, 'total': total})


def cuenta(request, id):
    try:
        cuenta = Cuenta.objects.get(pk=id)
    except Cuenta.DoesNotExist:
        raise Http404('La cuenta especificada no existe')
    return render(request, 'cuenta.html', {'cuenta': cuenta, 'movimientos': Movimiento.ultimos(id)}, )


def busqueda(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            limit = form.cleaned_data['limit']
            start = form.cleaned_data['dateStart']
            end = form.cleaned_data['dateEnd']
            movimientos = Movimiento.get_with(query, limit, start, end)
            form = SearchForm()
            return render(request, 'resultado.html', {'movimientos': movimientos, 'query': query, 'form': form})
    else:
        form = SearchForm()
    return render(request, 'busqueda.html', {'form': form})


def movimientos(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            return render(request, 'movimientos.html', {'movimientos': Movimiento.ultimos()})
    else:
        form = MovimientoForm()
        return render(request, 'get_movimientos.html', {'form': form})
