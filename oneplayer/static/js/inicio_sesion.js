document.addEventListener('DOMContentLoaded', function () {
    let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
    console.log(usuarios);

    // Formulario de inicio de sesión
    document.getElementById('inicio_sesion').addEventListener('submit', function (event) {
        event.preventDefault();

        const nombreUsuario = document.getElementById('nombre_usuario').value.trim();
        const passwordIngresado = document.getElementById('passwordsaved').value;
        const errorMensaje = document.getElementById('errorMensaje') || crearErrorMensaje();

        if (!nombreUsuario || !passwordIngresado) {
            errorMensaje.innerText = 'Por favor, ingresa un nombre de usuario y una contraseña.';
            errorMensaje.style.display = "block";
            return;
        }

        // Buscar el usuario en el localStorage
        const usuarioEncontrado = usuarios.find(usuario =>
            usuario.nombreUsuario === nombreUsuario &&
            usuario.password === passwordIngresado
        );

        if (!usuarioEncontrado) {
            errorMensaje.innerText = 'Nombre de usuario o contraseña incorrectos.';
            errorMensaje.style.display = "block";
            return;
        }

        // Guardar usuario activo y su rol
        localStorage.setItem('usuarioActivo', JSON.stringify(usuarioEncontrado));
        localStorage.setItem('logueado', 'true');
        localStorage.setItem('usuario', usuarioEncontrado.tipo_usuario); // administrador o cliente

        alert('Inicio de sesión exitoso. ¡Bienvenid@ ' + usuarioEncontrado.nombreUsuario + '!');

        // Redirección basada en el tipo de usuario
        if (usuarioEncontrado.tipo_usuario === "administrador") {
            window.location.href = "../user/gestion.html";
        } else {
            window.location.href = "../user/cuenta.html";
        }
    });

    // Función para crear mensaje de error
    function crearErrorMensaje() {
        const errorDiv = document.createElement("div");
        errorDiv.id = 'errorMensaje';
        errorDiv.style.color = 'red';
        errorDiv.style.marginTop = '10px';
        document.getElementById('inicio_sesion').appendChild(errorDiv);
        return errorDiv;
    }
});