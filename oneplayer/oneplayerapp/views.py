from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

from rest_framework import viewsets
from .models import Cliente, Administrador, Producto
from .serializers import ClienteSerializer, AdministradorSerializer, ProductoSerializer



# Vista Página Principal
def oneplayer_view(request):
    return render(request, 'ONEPLAYER.html')  


# Vista Categorías
def accion_view(request):
    return render(request, 'games/accion.html')

def carrera_view(request):
    return render(request, 'games/carrera.html')

def ftp_view(request):
    return render(request, 'games/ftp.html')

def ma_view(request):
    return render(request, 'games/ma.html')

def supervivencia_view(request):
    return render(request, 'games/supervivencia.html')

def terror_view(request):
    return render(request, 'games/terror.html')


# Vistas Autenticación
def inicio_sesion_view(request):
    return render(request, 'auth/inicio_sesion.html')

def registrarse_view(request):
    return render(request, 'auth/form_registro.html')


# Vistas Usuarios
def cuenta_view(request):
    return render(request, 'user/cuenta.html')

def contraseña_view(request):
    return render(request, 'user/contraseña.html')

def carrito_view(request):
    return render(request, 'user/carrito.html')

def gestion_view(request):
    return render(request, 'user/gestion.html')


# Vista Logout
def logout_view(request):
    logout(request)
    return redirect('inicio')


# Vista de la API
# Maneja GET y POS de objetos de los modelos
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer