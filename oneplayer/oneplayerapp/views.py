from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
import feedparser
import requests
from django.utils.timezone import make_aware
import datetime
import re

from .form_registro import CambiarContraseñaForm, EditarPerfilForm, RegistroUsuarioForm
from .forms import CategoriaForm, EditarCategoriaForm, ProductoForm
from .models import Administrador, Carrito, CarritoProducto, Categoria, Cliente, Compra, Producto, UsuariosRegistro

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

@login_required
def gestion_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'user/gestion.html', {'categorias': categorias})

def logout_view(request):
    logout(request)
    return redirect('inicio_sesion')

@login_required(login_url='/auth/inicio_sesion/')
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cliente = get_object_or_404(Cliente, nombre_usuario=request.user.username)
    cantidad = int(request.POST.get('cantidad', 1))

    carrito, creado = Carrito.objects.get_or_create(cliente=cliente, activo=True)
    carrito_producto, creado = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)

    if not creado:
        carrito_producto.cantidad += cantidad
    else:
        carrito_producto.cantidad = cantidad

    carrito_producto.save()

    total_items_carrito = carrito.items.count()
    return JsonResponse({'status': 'success', 'message': f"'{producto.nombre}' añadido al carrito.", 'total_items': total_items_carrito})
    return redirect('carrito')

@login_required
def carrito_view(request):
    try:
        cliente = Cliente.objects.get(usuariosregistro_ptr_id=request.user.id)
        carrito = Carrito.objects.get(cliente=cliente, activo=True)
        items_carrito = CarritoProducto.objects.filter(carrito=carrito)
        subtotal = sum([item.total() for item in items_carrito])
        total = subtotal
        return render(request, 'carrito.html', {'productos': items_carrito, 'subtotal': subtotal, 'total': total})
    except Cliente.DoesNotExist:
        return render(request, 'carrito.html', {'productos': [], 'mensaje': 'Tu perfil de cliente no existe.'})
    except Carrito.DoesNotExist:
        return render(request, 'carrito.html', {'productos': [], 'mensaje': 'Tu carrito está vacío.'})

@login_required
def eliminar_producto_carrito(request, producto_id):
    cliente = get_object_or_404(Cliente, nombre_usuario=request.user.username)
    carrito = get_object_or_404(Carrito, cliente=cliente)

    try:
        item = CarritoProducto.objects.get(carrito=carrito, producto_id=producto_id)
        item.delete()
    except CarritoProducto.DoesNotExist:
        pass

    return redirect('carrito')

@login_required
def finalizar_compra(request):
    cliente = get_object_or_404(Cliente, usuariosregistro_ptr_id=request.user.id)
    carrito = get_object_or_404(Carrito, cliente=cliente, activo=True)
    items_carrito = CarritoProducto.objects.filter(carrito=carrito)

    if not items_carrito.exists():
        messages.error(request, "El carrito está vacío. No puedes realizar la compra.")
        return redirect('carrito')

    total_compra = sum([item.total() for item in items_carrito])

    try:
        compra = Compra.objects.create(cliente=cliente, total=total_compra, fecha=timezone.now()) 
        carrito.activo = False
        carrito.save()
        items_carrito.delete() 

        messages.success(request, f"Compra realizada con éxito. Total: ${total_compra}")
        return redirect('checkout') 
    except Exception as e:
        messages.error(request, f"Ocurrió un error al procesar la compra: {e}")
        return redirect('checkout', compra_id=compra.id)

@login_required
def gestionar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'gestion', {'categorias': categorias})

@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría agregada correctamente.")
            return redirect('gestion')
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
            return redirect('gestion')
    else:
        form = EditarCategoriaForm(instance=categoria)
    return render(request, 'user/editar_categoria.html', {'form': form, 'categoria': categoria})

@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id) 
    if request.method == 'POST':
        categoria.delete() 
        return redirect('gestion') 
    return render(request, 'user/eliminar_categoria.html', {'categoria': categoria})

def registrarse_view(request):
    form = RegistroUsuarioForm()
    return render(request, 'auth/form_registro.html', {'form': form})

def registrar_usuario_vw(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            print(f"Valor de es_administrador recibido (ignorado): {form.cleaned_data.get('es_administrador')}")
            nombre_usuario = form.cleaned_data['nombre_usuario']
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            direccion = form.cleaned_data['direccion']
            contraseña = form.cleaned_data['contraseña']

            try:
                with transaction.atomic():
                    usuario_registro = UsuariosRegistro.objects.create(
                        nombre_usuario=nombre_usuario,
                        nombre=nombre,
                        email=email,
                        contraseña=make_password(contraseña),
                        es_administrador=False, 
                        direccion=direccion
                    )

                    user = User.objects.create_user(
                        username=nombre_usuario,
                        email=email,
                        password=contraseña
                    )

                Cliente.objects.create(
                    usuariosregistro_ptr_id=usuario_registro.id,
                    nombre_usuario=nombre_usuario,
                    nombre=nombre,
                    email=email,
                    direccion=direccion,
                    contraseña=contraseña
                )
                cliente = Cliente.objects.get(usuariosregistro_ptr_id=usuario_registro.id)
                carrito = Carrito.objects.create(cliente=cliente, activo=True)
                print(f"Carrito creado para el cliente {cliente.id} con ID {carrito.id}")

                messages.success(request, "Registro de cliente exitoso.")
                return redirect('inicio_sesion')

            except IntegrityError as e:
                if 'unique constraint' in str(e).lower() and 'nombre_usuario' in str(e).lower():
                    form.add_error('nombre_usuario', "Este nombre de usuario ya está en uso.")
                elif 'unique constraint' in str(e).lower() and 'email' in str(e).lower():
                    form.add_error('email', "Este correo electrónico ya está registrado.")
                else:
                    messages.error(request, "Ocurrió un error durante el registro. Por favor, inténtalo de nuevo.")
                return render(request, 'auth/form_registro.html', {'form': form})
        else:
            print(f"Errores del formulario: {form.errors}")
            return render(request, 'auth/form_registro.html', {'form': form})
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
            return redirect('user/cuenta.html')
        else:
            return render(request, 'editar_perfil', {'form': form})  
    else:
        form = EditarPerfilForm(instance=usuario) 
        return render(request, 'user/cuenta.html', {'form': form})

@login_required
def agregar_juego(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            juego = form.save(commit=False)
            juego.categoria = categoria 
            juego.save()
            messages.success(request, "Juego agregado correctamente.")
            return redirect('gestion') 
        else:
            messages.error(request, "Hubo un error en el formulario.")
            print(form.errors)
    else:
        form = ProductoForm()

    return render(request, 'user/agregar_juego.html', {'form': form, 'categoria': categoria})

@login_required
def gestion_view(request):
    categorias = Categoria.objects.prefetch_related('productos').all()
    return render(request, 'user/gestion.html', {'categorias': categorias})


def listar_accion(request):
    context = {}
    try:
        context['elden_ring'] = Producto.objects.get(nombre="Elden Ring")
    except Producto.DoesNotExist:
        context['elden_ring'] = None

    try:
        context['cyberpunk'] = Producto.objects.get(nombre="Cyberpunk 2077")
    except Producto.DoesNotExist:
        context['cyberpunk'] = None

    return render(request, 'games/accion.html', context)


def listar_carrera(request):
    context = {}
    try:
        context['mario_kart'] = Producto.objects.get(nombre="Mario Kart 8 Deluxe")
    except Producto.DoesNotExist:
        context['mario_kart'] = None

    try:
        context['sonic'] = Producto.objects.get(nombre="Sonic Racing")
    except Producto.DoesNotExist:
        context['sonic'] = None

    return render(request, 'games/carrera.html', context)


def listar_supervivencia(request):
    context = {}
    try:
        context['baldur'] = Producto.objects.get(nombre="Baldur's Gate 3")
    except Producto.DoesNotExist:
        context['baldur'] = None

    try:
        context['rust'] = Producto.objects.get(nombre="Rust") 
    except Producto.DoesNotExist:
        context['rust'] = None

    return render(request, 'games/supervivencia.html', context)



def listar_ftp(request):
    context = {}
    try:
        context['counter'] = Producto.objects.get(nombre="Counter-Strike 2")
    except Producto.DoesNotExist:
        context['counter'] = None

    try:
        context['marvel'] = Producto.objects.get(nombre="Marvel Rivals") 
    except Producto.DoesNotExist:
        context['marvel'] = None

    return render(request, 'games/FTP.html', context)


def listar_ma(request):
    context = {}
    try:
        context['monster'] = Producto.objects.get(nombre="Monster Hunter Wilds")
    except Producto.DoesNotExist:
        context['monster'] = None

    try:
        context['red'] = Producto.objects.get(nombre="Red Dead Redemption 2") 
    except Producto.DoesNotExist:
        context['red'] = None

    return render(request, 'games/MA.html', context)


def listar_terror(request):
    context = {}
    try:
        context['resident'] = Producto.objects.get(nombre="Resident Evil 4")
    except Producto.DoesNotExist:
        context['resident'] = None

    try:
        context['squid'] = Producto.objects.get(nombre="Terror Squid") 
    except Producto.DoesNotExist:
        context['squid'] = None

    return render(request, 'games/terror.html', context)



def vandal_noticias_view(request):
    vandal_feed_url = "https://vandal.elespanol.com/xml.cgi"
    
    # User-Agent personalizado
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MyApp/1.0; +https://example.com)'
    }
    try:
        response = requests.get(vandal_feed_url, headers=headers, timeout=10)
        response.raise_for_status() 
        feed = feedparser.parse(response.content)
    except Exception as e:
        print(f"Error al obtener o parsear el feed: {e}")
        feed = feedparser.parse("") 

    noticias_vandal = []
    for entry in feed.entries[:5]:
        titulo = entry.get('title', 'Sin título')
        link = entry.get('link', '#')
        descripcion = entry.get('description', 'Sin descripción')
        fecha_str = entry.get('published') or entry.get('pubdate')
        fecha = None
        if fecha_str:
            try:
                fecha = make_aware(datetime.datetime(*feedparser._parse_date(fecha_str)[:6]))
            except Exception as e:
                print(f"Error al parsear la fecha: {e}")
                fecha = 'Fecha desconocida'
        else:
            fecha = 'Fecha desconocida'

        imagen_url = None
        descripcion_resumen = 'Sin descripción'
        if descripcion:
            img_match = re.search(r'<img.*?src="(.*?)"', descripcion)
            if img_match:
                imagen_url = img_match.group(1)
            descripcion_sin_html = re.sub('<[^<]+?>', '', descripcion).strip()
            descripcion_resumen = descripcion_sin_html[:150] + '...' if len(descripcion_sin_html) > 150 else descripcion_sin_html

        noticia = {
            'titulo': titulo,
            'link': link,
            'descripcion': descripcion_resumen,
            'fecha': fecha if not isinstance(fecha, str) else fecha,
            'imagen_url': imagen_url
        }
        noticias_vandal.append(noticia)

    context = {'noticias_vandal': noticias_vandal, 'fuente': 'Vandal'}
    return render(request, 'ONEPLAYER.html', context)



'''
def vandal_noticias_view(request):
    vandal_feed_url = "https://vandal.elespanol.com/xml.cgi"
    feed = feedparser.parse(vandal_feed_url)
    noticias_vandal = []
    for entry in feed.entries[:5]:
        titulo = entry.get('title', 'Sin título')
        link = entry.get('link', '#')
        descripcion = entry.get('description', 'Sin descripción')
        fecha_str = entry.get('published') or entry.get('pubdate')
        fecha = None
        if fecha_str:
            try:
                fecha = make_aware(datetime.datetime(*feedparser._parse_date(fecha_str)[:6]))
            except Exception as e:
                print(f"Error al parsear la fecha: {e}")
                fecha = 'Fecha desconocida'
        else:
            fecha = 'Fecha desconocida'

        # Intenta extraer la primera imagen de la descripción (más robusto)
        imagen_url = None
        if descripcion:
            img_match = re.search(r'<img.*?src="(.*?)"', descripcion)
            if img_match:
                imagen_url = img_match.group(1)
            # Elimina las etiquetas HTML de la descripción para mostrar un resumen
            descripcion_sin_html = re.sub('<[^<]+?>', '', descripcion).strip()
            # Trunca la descripción para el resumen
            descripcion_resumen = descripcion_sin_html[:150] + '...' if len(descripcion_sin_html) > 150 else descripcion_sin_html

        noticia = {
            'titulo': titulo,
            'link': link,
            'descripcion': descripcion_resumen, # Usamos el resumen
            'fecha': fecha if not isinstance(fecha, str) else fecha,
            'imagen_url': imagen_url
        }
        noticias_vandal.append(noticia)

    context = {'noticias_vandal': noticias_vandal, 'fuente': 'Vandal'}
    return render(request, 'inicio', context)
'''