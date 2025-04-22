from django import forms
from .models import Categoria, Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre del producto'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Descripción del producto'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio del producto'})
        self.fields['stock'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Stock inicial'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'})

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre'] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre de la categoría',
        })

class EditarCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingrese el nuevo nombre de la categoría',
        })