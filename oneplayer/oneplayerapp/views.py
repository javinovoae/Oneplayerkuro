from django.shortcuts import render


# Vista Página Principal
def oneplayer_view(request):
    return render(request, 'ONEPLAYER.html')  


# Vista Categorías
def accion_view(request):
    return render(request, 'game/accion.html')

def carrera_view(request):
    return render(request, 'game/carrera.html')

def ftp_view(request):
    return render(request, 'game/ftp.html')

def ma_view(request):
    return render(request, 'game/ma.html')

def supervivencia_view(request):
    return render(request, 'game/supervivencia.html')

def terror_view(request):
    return render(request, 'game/terror.html')


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
