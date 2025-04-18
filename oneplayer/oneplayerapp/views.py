from django.shortcuts import render

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .form_registro import RegistroUsuarioForm
from .models import UsuariosRegistro

from .models import Carrito, CarritoProducto, Cliente, Producto, Categoria, Administrador

#from rest_framework import viewsets
#from .serializers import ClienteSerializer, AdministradorSerializer, ProductoSerializer



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

#Vista Usuario 


def registrarse_view(request):
    form = RegistroUsuarioForm()  # Crea una instancia del formulario
    return render(request, 'auth/form_registro.html', {'form': form})  # Pasa el formulario al contexto


def registrar_usuario_vw(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        print(f"¿El formulario es válido? {form.is_valid()}")
        print(f"Errores del formulario: {form.errors}")
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            email = form.cleaned_data['email']
            nombre_completo = form.cleaned_data['nombre']
            contraseña = form.cleaned_data['contraseña']
            es_administrador = form.cleaned_data['es_administrador']
            try:
                user = User.objects.create_user(username=nombre_usuario, email=email, password=contraseña)
                usuario = UsuariosRegistro(
                    nombre_usuario=nombre_usuario,
                    nombre=nombre_completo,
                    email=email,
                    contraseña=contraseña,  # Se hasheará al guardar
                    es_administrador=es_administrador
                )
                usuario.save()
                messages.success(request, "Usuario registrado con éxito!")
                print("Redirigiendo a inicio_sesion")  # <--- Añade este print
                return redirect('inicio_sesion')
            except Exception as e:
                print(f"Error al crear la cuenta: {e}")
                form.add_error(None, f"Ocurrió un error inesperado al crear la cuenta: {e}")
                print("Renderizando formulario con error (except)")  # <--- Añade este print
                return render(request, 'auth/form_registro.html', {'form': form})
        else:
            print("Renderizando formulario inválido")  # <--- Añade este print
            return render(request, 'auth/form_registro.html', {'form': form})
    else:
        print("Renderizando formulario GET")  # <--- Añade este print
        form = RegistroUsuarioForm()
        return render(request, 'auth/form_registro.html', {'form': form})

# Cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio_sesion')


# Editar perfil
@login_required
def editar_perfil(request):
    # Obtener el perfil del usuario autenticado
    try:
        usuario = UsuariosRegistro.objects.get(nombre_usuario=request.user.username)
    except UsuariosRegistro.DoesNotExist:
        messages.error(request, "No se encontró el usuario.")
        return redirect('menu_principal_view')  

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=usuario)  # Rellenar con los datos actuales del usuario
        if form.is_valid():
            form.save()  # Guardar los cambios
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('micuenta_view')  # Redirigir a mi cuenta
    else:
        form = EditarPerfilForm(instance=usuario)  # Rellenar con los datos actuales del usuario

    return render(request, 'editar_perfil.html', {'form': form})
