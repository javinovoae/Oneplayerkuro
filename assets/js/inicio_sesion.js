document.addEventListener('DOMContentLoaded', function() {
    // Obtener usuarios almacenados en localStorage
    let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];

    // Verificar si no existen usuarios y agregar un usuario administrador por defecto
    if (usuarios.length === 0) {
        const usuarioAdministrador = {
            nombreUsuario: 'admin',
            password: 'admin123', 
            nombreCompleto: 'Administrador', 
            fechaNacimiento: '12-12-1991',
            correo: 'admin@oneplayer.com', 
            role: 'admin' 
        };
        usuarios.push(usuarioAdministrador); 
        localStorage.setItem('usuarios', JSON.stringify(usuarios)); // Guardar en localStorage
    }

    // Manejador de evento para el formulario de inicio de sesión
    document.getElementById('inicio_sesion').addEventListener('submit', function (event) {
        event.preventDefault(); // Evita el envío del formulario por defecto

        const nombreUsuario = document.getElementById('nombre_usuario').value.trim();
        const passwordIngresado = document.getElementById('passwordsaved').value;
        const errorMensaje = document.getElementById('errorMensaje') || crearErrorMensaje();

        // Validar que el formulario no esté vacío
        if (!nombreUsuario || !passwordIngresado) {
            errorMensaje.innerText = 'Por favor, ingresa un nombre de usuario y una contraseña.';
            errorMensaje.style.display = "block";
            return;
        }

        // Buscar si el usuario existe y la contraseña coincide
        const usuarioEncontrado = usuarios.find(usuario => usuario.nombreUsuario === nombreUsuario && usuario.password === passwordIngresado);

        if (!usuarioEncontrado) {
            errorMensaje.innerText = 'Nombre de usuario o contraseña incorrectos.';
            errorMensaje.style.display = "block";
            return;
        }

        // Guardar la información del usuario activo en localStorage
        localStorage.setItem('usuarioActivo', JSON.stringify(usuarioEncontrado));

        alert('Inicio de sesión exitoso. ¡Bienvenid@ ' + usuarioEncontrado.nombreUsuario + '!');

let usuario = "admin";

if (usuario === "admin") {
    window.location.href = "../user/usuarios.html"; 
} else {
    window.location.href = "../ONEPLAYER.html#categorias?logged=true";
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
