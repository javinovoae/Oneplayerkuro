document.getElementById('formulario').addEventListener('submit', function (event) {
    event.preventDefault(); // Evitar el envío automático del formulario

    const password = document.getElementById('password').value;
    const password2 = document.getElementById('password2').value;
    const correo = document.getElementById('correo').value;
    const fechaNacimiento = document.getElementById('fecha_nac').value;
    const errorMensaje = document.getElementById('errorMensaje');

    errorMensaje.innerText = "";
    errorMensaje.style.display = "none";

    // Validación de edad
    const fechaActual = new Date();
    const fechaIngresada = new Date(fechaNacimiento);

    const edad = fechaActual.getFullYear() - fechaIngresada.getFullYear();
    const diferenciaMes = fechaActual.getMonth() - fechaIngresada.getMonth();
    const diferenciaDia = fechaActual.getDate() - fechaIngresada.getDate();

    if (
        edad < 13 ||
        (edad === 13 && diferenciaMes < 0) ||
        (edad === 13 && diferenciaMes === 0 && diferenciaDia < 0)
    ) {
        errorMensaje.innerText = "Debes tener al menos 13 años para registrarte.";
        errorMensaje.style.display = "block";
        return; // Detener el envío del formulario
    }

    // Validación de correo electrónico
    const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regexCorreo.test(correo)) {
        errorMensaje.innerText = "Por favor, ingresa un correo electrónico válido.";
        errorMensaje.style.display = "block";
        return;
    }

    // Validación de contraseña
    const regexPassword = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{6,18}$/;
    if (!regexPassword.test(password)) {
        errorMensaje.innerHTML = "La contraseña debe contener al menos:<ul><li>Entre 6 y 18 caracteres</li><li>1 número</li><li>1 letra mayúscula</li><li>1 carácter especial</li></ul>";
        errorMensaje.style.display = "block";
        return;
    }

    if (password !== password2) {
        errorMensaje.innerText = "Las contraseñas no coinciden.";
        errorMensaje.style.display = "block";
        return;
    }

    // Si todas las validaciones pasan, redirigir a la página de inicio
    alert("Formulario enviado correctamente.");
    window.location.href = "./GAME.html"; 

});
