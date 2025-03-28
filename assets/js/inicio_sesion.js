
document.getElementById('inicio_sesion').addEventListener('submit', function (event) {
    event.preventDefault(); // Evita el envío del formulario por defecto

    const nombreUsuario = document.getElementById('nombre_usuario').value.trim();
    const passwordIngresado = document.getElementById('passwordsaved').value;
    const errorMensaje = document.getElementById('errorMensaje') || crearErrorMensaje();


    // Obtener usuarios almacenados en localStorage
    let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];


    // Buscar si el usuario existe y la contraseña coincide
    const usuarioEncontrado = usuarios.find(usuario => usuario.nombreUsuario === nombreUsuario && usuario.password === passwordIngresado);

    if (!usuarioEncontrado) {
        errorMensaje.innerText = 'Nombre de usuario o contraseña incorrectos.';
        errorMensaje.style.display = "block";
        return;
    }

    localStorage.setItem('usuarioActivo', JSON.stringify(usuarioEncontrado));

    alert('Inicio de sesión exitoso. ¡Bienvenid@ ' + usuarioEncontrado.nombreUsuario + '!');

    window.location.href = "../ONEPLAYER.html#categorias?logged=true";
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