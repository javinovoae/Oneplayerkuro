# from rest_framework import viewsets
# from .serializers import ClienteSerializer, AdministradorSerializer, ProductoSerializer

# Vista de la API
# class ClienteViewSet(viewsets.ModelViewSet):
#     queryset = Cliente.objects.all()
#     serializer_class = ClienteSerializer

# class AdministradorViewSet(viewsets.ModelViewSet):
#     queryset = Administrador.objects.all()
#     serializer_class = AdministradorSerializer

# class ProductoViewSet(viewsets.ModelViewSet):
#     queryset = Producto.objects.all()
#     serializer_class = ProductoSerializer

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .form_registro import EditarPerfilForm
from .form_registro import RegistroUsuarioForm
from django.contrib.auth.forms import AuthenticationForm
from .models import UsuariosRegistro, Carrito, CarritoProducto, Cliente, Producto, Categoria, Administrador
from .form_registro import CambiarContraseñaForm
from django.shortcuts import render
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from .models import Producto, Carrito, CarritoProducto, Cliente


@login_required
def mi_cuenta(request):
    return render(request, 'mi_cuenta.html', {
        'usuario': request.user,
    })

def oneplayer_view(request):
    return render(request, 'ONEPLAYER.html')  

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

def inicio_sesion_view(request):
    if request.method == 'POST':
        username = request.POST['nombre']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'inicio') 
            return redirect(next_url)
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return redirect('inicio_sesion')

    return render(request, 'auth/inicio_sesion.html')

@login_required
def cuenta_view(request):
    try:
        usuario_registro = UsuariosRegistro.objects.get(nombre_usuario=request.user.username)
        form = EditarPerfilForm(instance=usuario_registro)
    except UsuariosRegistro.DoesNotExist:
        form = EditarPerfilForm()  

    return render(request, 'user/cuenta.html', {
        'usuario': request.user,
        'form': form,
    })

def carrito_view(request):
    return render(request, 'user/carrito.html')

def gestion_view(request):
    return render(request, 'user/gestion.html')

def logout_view(request):
    logout(request)
    return redirect('inicio_sesion')

@login_required(login_url='/auth/inicio_sesion/')
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cliente = get_object_or_404(Cliente, usuario=request.user)
    cantidad = int(request.POST.get('cantidad', 1))

    carrito, creado = Carrito.objects.get_or_create(cliente=cliente, activo=True)
    carrito_producto, creado = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)

    if not creado:
        carrito_producto.cantidad += cantidad
    else:
        carrito_producto.cantidad = cantidad

    carrito_producto.save()
    return redirect('carrito')

@login_required(login_url='/auth/inicio_sesion/')
def carrito_view(request):
    try:
        cliente = Cliente.objects.get(nombre_usuario=request.user.username)
        carrito = Carrito.objects.get(cliente=cliente, activo=True)
        productos = carrito.productos.all()
        total = sum(item.total() for item in productos)
        return render(request, 'user/carrito.html', {
            'carrito': carrito,
            'productos': productos,
            'total': total,
            'carrito_vacio': not productos.exists()
        })
    except (Cliente.DoesNotExist, Carrito.DoesNotExist):
        return render(request, 'user/carrito.html', {
            'carrito': None,
            'productos': [],
            'total': 0,
            'carrito_vacio': True
        })

def registrarse_view(request):
    form = RegistroUsuarioForm()
    return render(request, 'auth/form_registro.html', {'form': form})

def registrar_usuario_vw(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            email = form.cleaned_data['email']
            nombre_completo = form.cleaned_data['nombre']
            direccion = form.cleaned_data['direccion']
            contraseña = form.cleaned_data['contraseña']
            es_administrador = form.cleaned_data['es_administrador']

            try:
                user = User.objects.create_user(username=nombre_usuario, email=email, password=contraseña)
                usuario = UsuariosRegistro(
                    nombre_usuario=nombre_usuario,
                    nombre=nombre_completo,
                    email=email,
                    direccion=direccion,
                    contraseña=contraseña,
                    es_administrador=es_administrador
                )
                usuario.save()
                messages.success(request, "Usuario registrado con éxito!")
                return redirect('inicio_sesion')
            except Exception as e:
                form.add_error(None, f"Ocurrió un error inesperado al crear la cuenta: {e}")
                return render(request, 'auth/form_registro.html', {'form': form})
        else:
            return render(request, 'auth/form_registro.html', {'form': form})
    else:
        form = RegistroUsuarioForm()
        return render(request, 'auth/form_registro.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio_sesion')


@login_required
def editar_perfil_org(request):
    try:
        usuario = UsuariosRegistro.objects.get(nombre_usuario=request.user.username)
    except UsuariosRegistro.DoesNotExist:
        messages.error(request, "No se encontró el usuario.")
        return redirect('inicio')

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('cuenta')
        else:
            return render(request, 'editar_perfil', {'form': form})  
    else:
        form = EditarPerfilForm(instance=usuario) 
        return render(request, 'cuenta', {'form': form})  

def checkout_view(request):
    return render(request, 'user/checkout.html')

@login_required
def editar_contraseña_org(request):
    if request.method == 'POST':
        form = CambiarContraseñaForm(request.POST)
        form.request = request  
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('cuenta')  
        else:
            return render(request, 'user/contraseña.html', {'form': form})
    else:
        return redirect('user/contraseña.html') 
    

@login_required
def cambiar_contraseña_view(request):
    form = CambiarContraseñaForm()
    return render(request, 'user/contraseña.html', {'form': form})

#CARRITO LOGICA

@login_required
def agregar_al_carrito(request, producto_id):
    cliente = get_object_or_404(Cliente, nombre_usuario=request.user.username)
    producto = get_object_or_404(Producto, id=producto_id)


    carrito, creado = Carrito.objects.get_or_create(cliente=cliente)

    item, creado = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)

    if not creado:
        item.cantidad += 1
        item.save()

    return redirect('ver_carrito') 

#mostrar el producto

@login_required
def ver_carrito(request):
    cliente = get_object_or_404(Cliente, nombre_usuario=request.user.username)
    carrito, creado = Carrito.objects.get_or_create(cliente=cliente)

    productos = carrito.productos.all()
    subtotal = sum([p.total() for p in productos])
    
    return render(request, 'carrito.html', {
        'productos': productos,
        'subtotal': subtotal,
        'total': subtotal  
    })

#eliminar productos

@login_required 
def eliminar_producto_carrito(request, producto_id):
    cliente = get_object_or_404(Cliente, nombre_usuario=request.user.username)
    carrito = get_object_or_404(Carrito, cliente=cliente)

    item = get_object_or_404(CarritoProducto, carrito=carrito, producto_id=producto_id)
    item.delete()

    return redirect('ver_carrito')

#finalizar compra y vaciar carrito
@login_required
def finalizar_compra(request):
    cliente = get_object_or_404(Cliente, nombre_usuario=request.user.username)
    carrito = get_object_or_404(Carrito, cliente=cliente)

    productos = carrito.productos.all()
    if not productos.exists():
        return redirect('ver_carrito')

    total_compra = sum([p.total() for p in productos])

    # Guardar el total de la compra
    Compra.objects.create(cliente=cliente, total=total_compra)

    # Vaciar el carrito
    productos.delete()

    return render(request, 'user/checkout.html', {'total': total_compra})

