from django.shortcuts import render

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from .models import Carrito, CarritoProducto, Cliente, Producto, Categoria, Administrador

#from rest_framework import viewsets
#from .serializers import ClienteSerializer, AdministradorSerializer, ProductoSerializer



# Vista Página Principal
def oneplayer_view(request):
    return render(request, 'ONEPLAYER.html')  


# Vista Categorías
def accion_view(request):
    categoria_accion = Categoria.objects.get(nombre='Acción')
    productos_accion = Producto.objects.filter(categoria=categoria_accion)[:2]  
    return render(request, 'games/accion.html', {'productos': productos_accion})

def carrera_view(request):
    categoria_carrera = Categoria.objects.get(nombre='Carrera')
    productos_carrera = Producto.objects.filter(categoria=categoria_carrera)[:2]  
    return render(request, 'games/carrera.html', {'productos': productos_carrera})

def ftp_view(request):
    categoria_ftp = Categoria.objects.get(nombre='FTP')
    productos_ftp = Producto.objects.filter(categoria=categoria_ftp)[:2] 
    return render(request, 'games/ftp.html', {'productos': productos_ftp})

def ma_view(request):
    categoria_ma = Categoria.objects.get(nombre='MA')
    productos_ma = Producto.objects.filter(categoria=categoria_ma)[:2]  
    return render(request, 'games/ma.html', {'productos': productos_ma})

def supervivencia_view(request):
    categoria_supervivencia = Categoria.objects.get(nombre='Supervivencia')
    productos_supervivencia = Producto.objects.filter(categoria=categoria_supervivencia)[:2]  
    return render(request, 'games/supervivencia.html', {'productos': productos_supervivencia})

def terror_view(request):
    categoria_terror = Categoria.objects.get(nombre='Terror')
    productos_terror = Producto.objects.filter(categoria=categoria_terror)[:2]  
    return render(request, 'games/terror.html', {'productos': productos_terror})



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


# Vista para Agregar al Carrito
@login_required(login_url='/iniciar_sesion/')
def agregar_al_carrito(request, producto_id):
    # Obtener el producto y el cliente
    producto = get_object_or_404(Producto, id=producto_id)
    cliente = get_object_or_404(Cliente, usuario=request.user)

    cantidad = int(request.POST.get('cantidad', 1))

    # Obtener o crear el carrito del cliente
    carrito, creado = Carrito.objects.get_or_create(cliente=cliente, activo=True)

    # Obtener o crear el producto dentro del carrito
    carrito_producto, creado = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)

    if not creado:
        carrito_producto.cantidad += cantidad
    else:
        carrito_producto.cantidad = cantidad

    carrito_producto.save()

    return redirect('carrito')


# Vista para Carrito
@login_required(login_url='iniciar_sesion') 
def carrito_view(request):
    try:
        carrito = Carrito.objects.get(cliente=request.user.cliente, activo=True)
        productos = carrito.productos.all()
        total = sum(item.total() for item in productos)
        return render(request, 'carrito.html', {
            'carrito': carrito,
            'productos': productos,
            'total': total,
            'carrito_vacio': not productos.exists()
        })
    except Carrito.DoesNotExist:
        return render(request, 'carrito.html', {
            'carrito': None,
            'productos': [],
            'total': 0,
            'carrito_vacio': True
        })


# Vista de la API
#class ClienteViewSet(viewsets.ModelViewSet):
#    queryset = Cliente.objects.all()
#    serializer_class = ClienteSerializer

#class AdministradorViewSet(viewsets.ModelViewSet):
#    queryset = Administrador.objects.all()
#    serializer_class = AdministradorSerializer

#class ProductoViewSet(viewsets.ModelViewSet):
#    queryset = Producto.objects.all()
#    serializer_class = ProductoSerializer