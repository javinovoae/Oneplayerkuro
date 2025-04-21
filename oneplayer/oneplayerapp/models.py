from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone

# Modelo base de la tabla de django 
class UsuariosRegistro(models.Model):
    nombre_usuario = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    direccion = models.CharField(max_length=80)
    contraseña = models.CharField(max_length=30) 
    
    # Indicamos si el usuario es un administrador o cliente
    es_administrador = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
    

    def save(self, *args, **kwargs):
        # Hashea la contraseña antes de guardar
        self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)


class Cliente(UsuariosRegistro):
    carrito = models.OneToOneField('Carrito', on_delete=models.CASCADE, related_name='cliente_carrito', null=True, blank=True)
    def __str__(self):
        return f"Cliente: {self.nombre}"


class Administrador(UsuariosRegistro):
    def __str__(self):
        return f"Administrador: {self.nombre}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='carrito_cliente') 
    activo = models.BooleanField(default=True)  
    def __str__(self):
        return f"Carrito de {self.cliente.nombre}"


class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"Producto: {self.producto.nombre} - Cantidad: {self.cantidad} en carrito de {self.carrito.cliente.nombre}"
    def total(self):
        return self.producto.precio * self.cantidad

class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra de {self.cliente.nombre} - Total: ${self.total} - Fecha: {self.fecha.strftime('%Y-%m-%d')}"
    
    