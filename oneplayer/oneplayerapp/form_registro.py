from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
import re
from .models import UsuariosRegistro

def username_no_repetido_validator(value, user=None):
    if user is None:
        if User.objects.filter(username=value).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
    else:
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")

def email_no_repetido_validator(value, user=None):
    if user is None:
        if User.objects.filter(email=value).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
    else:
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")

class SoloLetrasEspaciosValidator:
    def __call__(self, value):
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")

class PasswordSymbolValidator:
    def __call__(self, value):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise forms.ValidationError("La contraseña debe contener al menos un caracter especial.")

class RegistroUsuarioForm(forms.Form):
    nombre_usuario = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre de Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[MinLengthValidator(2, "El nombre de usuario debe tener al menos 2 caracteres."),
                    MaxLengthValidator(15, "El nombre de usuario no puede tener más de 15 caracteres.")]
    )

    nombre = forms.CharField(
        required=True,
        label='Nombre Completo',
        max_length=30,
        validators=[MinLengthValidator(2, "El nombre debe tener al menos 2 caracteres."),
                    SoloLetrasEspaciosValidator()]
    )

    email = forms.EmailField(
        required=True,
        label='Correo Electrónico',
        max_length=50,
    )

    direccion = forms.CharField(
        required=True,
        label='Dirección',
        max_length=80,
        validators=[MinLengthValidator(2, "La dirección debe tener al menos 2 caracteres."),
                    SoloLetrasEspaciosValidator()]
    )

    contraseña = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Contraseña',
        validators=[MinLengthValidator(6, "La contraseña debe tener al menos 6 caracteres."),
                    MaxLengthValidator(12, "La contraseña no puede tener más de 12 caracteres."),
                    PasswordSymbolValidator()]
    )

    confirmar_contraseña = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Confirmar Contraseña'
    )

    es_administrador = forms.ChoiceField(
        label='Tipo de Cuenta',
        choices=[(False, 'Cliente'), (True, 'Administrador')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if contraseña and confirmar_contraseña and contraseña != confirmar_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

#ESTO SE ESTA EDITANDO AHORA 
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = UsuariosRegistro
        fields = ['nombre', 'email','direccion']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            user = User.objects.filter(username=self.instance.nombre_usuario).first()
            email_no_repetido_validator(email, user)
        return email