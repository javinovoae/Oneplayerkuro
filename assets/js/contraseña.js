    // Función que muestra u oculta la contraseña 
    function togglePassword(id, btn) {
        const input = document.getElementById(id);
        const icon = btn.querySelector('span');

        if (input.type === "password") {
            input.type = "text";
            icon.textContent = "🙈";  // ícono de ocultar
        } else {
            input.type = "password";
            icon.textContent = "👁️";  // ícono de mostrar
        }
    }

function cambiarContraseña() {
    // Obtener el usuario logueado
    const usuarioLogueado = JSON.parse(localStorage.getItem("usuarioActivo"));
    if (!usuarioLogueado) {
        alert("No se encontró el usuario o no está logueado");
        return;
    }

    // Obtener contraseñas
    const passwordGuardada = usuarioLogueado.password;
    const passwordActualInput = document.getElementById('edit_password_current').value;
    const edit_password = document.getElementById('edit_password').value;
    const edit_password2 = document.getElementById('edit_password2').value;
    const errorMensaje = document.getElementById('error_mensaje');

    // Validar la coincidencia de la contraseña antigua 
    if (passwordActualInput !== passwordGuardada) {
        errorMensaje.innerText = "La contraseña actual es incorrecta.";
        errorMensaje.style.display = "block";
        return;
    }

    // Validar la contraseña nueva
    const regexPassword = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{6,18}$/;
    if (!regexPassword.test(edit_password)) {
        errorMensaje.innerHTML = "La contraseña debe contener al menos:<ul><li>Entre 6 y 18 caracteres</li><li>1 número</li><li>1 letra mayúscula</li><li>1 carácter especial</li></ul>";
        errorMensaje.style.display = "block";
        return;
    }

    // Ver si las contraseñas son iguales
    if (edit_password !== edit_password2) {
        errorMensaje.innerText = "Las contraseñas no coinciden";
        errorMensaje.style.display = "block";
        return;
    }

    // Actualizar la contraseña
    usuarioLogueado.password = edit_password;

    // Guardar los cambios en el localStorage
    let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];
    const usuarioIndex = usuarios.findIndex(u => u.nombreUsuario === usuarioLogueado.nombreUsuario);

    if (usuarioIndex !== -1) {
        usuarios[usuarioIndex].password = edit_password;
        localStorage.setItem("usuarios", JSON.stringify(usuarios));
    }

    // Actualizar la sesión activa con la nueva contraseña
    localStorage.setItem("usuarioActivo", JSON.stringify(usuarioLogueado));

    // Limpiar el mensaje de error
    errorMensaje.style.display = "none";

    // Confirmar éxito
    alert("Contraseña cambiada con éxito");

    // Redirigir a la página de inicio de sesión
    window.location.href = "../auth/inicio_sesion.html";
}