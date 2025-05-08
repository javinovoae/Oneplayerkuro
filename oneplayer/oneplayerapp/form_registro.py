from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
import re
from .models import UsuariosRegistro
from django.contrib.auth import authenticate, get_user_model


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
            raise forms.ValidationError("Solo puede contener letras y espacios.")

class PasswordSymbolValidator:
    def __call__(self, value):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise forms.ValidationError("La contraseña debe contener al menos un caracter especial.")


#REGISTRO DE USUARIOS
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
        choices=[(False, 'Cliente'), (True, 'Administrador')],
        widget=forms.RadioSelect,
        required=False,  
        initial=False    
    )


    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if contraseña and confirmar_contraseña and contraseña != confirmar_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            nombre_usuario = self.cleaned_data.get('nombre_usuario')
            user = User.objects.filter(username=nombre_usuario).first()
            email_no_repetido_validator(email, user)
        return email
    

# EDICIÓN DE INFORMACIÓN
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = UsuariosRegistro
        fields = ['nombre', 'email','direccion']


# EDICION DE CONTRASEÑA
User = get_user_model()

class CambiarContraseñaForm(forms.Form):
    contraseña_actual = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_contraseña_actual', 'class': 'form-control'}),
        label='Contraseña Actual',
        required=True
    )
    nueva_contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_nueva_contraseña', 'class': 'form-control'}),
        label='Nueva Contraseña',
        required=True,
        validators=[MinLengthValidator(6, "La contraseña debe tener al menos 6 caracteres."),
                    MaxLengthValidator(12, "La contraseña no puede tener más de 12 caracteres."),
                    PasswordSymbolValidator()]
    )
    confirmar_nueva_contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_confirmar_nueva_contraseña', 'class': 'form-control'}),
        label='Repetir Nueva Contraseña',
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get("nueva_contraseña")
        confirmar_nueva_contraseña = cleaned_data.get("confirmar_nueva_contraseña")
        contraseña_actual = cleaned_data.get("contraseña_actual")

        if nueva_contraseña and confirmar_nueva_contraseña and nueva_contraseña != confirmar_nueva_contraseña:
            raise forms.ValidationError("Las nuevas contraseñas no coinciden.")

        # Validar que la nueva contraseña no sea igual a la actual
        if contraseña_actual and nueva_contraseña and contraseña_actual == nueva_contraseña:
            raise forms.ValidationError("La nueva contraseña no puede ser igual a la contraseña actual.")

        return cleaned_data

    def clean_contraseña_actual(self):
        contraseña_actual = self.cleaned_data.get('contraseña_actual')
        user = self.request.user
        if not authenticate(username=user.username, password=contraseña_actual):
            raise forms.ValidationError("Tu contraseña actual es incorrecta.")
        return contraseña_actual

    def save(self):
        user = self.request.user
        nueva_contraseña = self.cleaned_data.get('nueva_contraseña')
        user.set_password(nueva_contraseña)
        user.save()
