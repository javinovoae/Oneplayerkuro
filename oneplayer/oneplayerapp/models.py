from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # Indicamos si el usuario es un administrador o cliente
    es_administrador = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre

class Cliente(Usuario):
    carrito = models.ManyToManyField('Producto', through='Carrito')  # Relación con los productos en el carrito

    def __str__(self):
        return f"Cliente: {self.nombre}"

class Administrador(Usuario):
    def __str__(self):
        return f"Administrador: {self.nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Carrito de {self.cliente.nombre} - Producto: {self.producto.nombre}"
