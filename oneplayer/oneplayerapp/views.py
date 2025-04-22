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

from .form_registro import EditarPerfilForm, RegistroUsuarioForm, CambiarContraseñaForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UsuariosRegistro, Carrito, CarritoProducto, Cliente, Producto, Categoria, Administrador, Compra
from .forms import CategoriaForm, EditarCategoriaForm
from decimal import Decimal

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

@login_required
def eliminar_producto_carrito(request, producto_id):
    cliente = get_object_or_404(Cliente, nombre_usuario=request.user.username)
    carrito = get_object_or_404(Carrito, cliente=cliente)

    item = get_object_or_404(CarritoProducto, carrito=carrito, producto_id=producto_id)
    item.delete()

    return redirect('ver_carrito')

@login_required
def finalizar_compra(request):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    carrito = get_object_or_404(Carrito, cliente=cliente, activo=True)

    productos = carrito.productos.all()
    if not productos.exists():
        messages.error(request, "El carrito está vacío. No puedes realizar la compra.")
        return redirect('ver_carrito')

    total_compra = sum([p.total() for p in productos])

    try:
        compra = Compra.objects.create(cliente=cliente, total=total_compra)
        carrito.activo = False
        carrito.save()

        productos.delete()

        messages.success(request, f"Compra realizada con éxito. Total: ${total_compra}")
        return redirect('checkout_view')
    except Exception as e:
        messages.error(request, f"Ocurrió un error al procesar la compra: {e}")
        return redirect('ver_carrito')

@login_required
def gestionar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'user/gestion.html', {'categorias': categorias})

@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría agregada correctamente.")
            return redirect('gestion_categorias')
        else:
            messages.error(request, "Por favor, ingresa un nombre válido para la categoría.")
    else:
        form = CategoriaForm()
    return render(request, 'user/agregar_categoria.html', {'form': form})

@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        form = EditarCategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría editada correctamente.")
            return redirect('gestion_categorias')
    else:
        form = EditarCategoriaForm(instance=categoria)
    return render(request, 'user/editar_categoria.html', {'form': form, 'categoria': categoria})

@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id) 
    if request.method == 'POST':
        categoria.delete() 
        return redirect('gestion_categorias') 
    return render(request, 'user/eliminar_categoria.html', {'categoria': categoria})

def registrarse_view(request):
    form = RegistroUsuarioForm()
    return render(request, 'auth/form_registro.html', {'form': form})
def registrar_usuario_vw(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():

            form.save()
            messages.success(request, "Registro exitoso.")
            return redirect('inicio_sesion')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'auth/form_registro.html', {'form': form})

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
        form = CambiarContraseñaForm()
        return render(request, 'user/contraseña.html', {'form': form})
    
@login_required
def cambiar_contraseña_view(request):
    form = CambiarContraseñaForm()
    return render(request, 'user/contraseña.html', {'form': form})

@login_required
def checkout_view(request):
    return render(request, 'user/checkout.html')

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

