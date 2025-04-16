document.getElementById('formulario').addEventListener('submit', function (event) {
    event.preventDefault(); // Evitar el envío automático del formulario

    const tipoUsuario = document.getElementById('tipo_usuario').value;
    const nombreUsuario = document.getElementById('nombre_usuario').value.trim();
    const nombreCompleto = document.getElementById('nombre_completo').value.trim();
    const fechaNacimiento = document.getElementById('fecha_nac').value;
    const correo = document.getElementById('correo').value;
    const direccion = document.getElementById('direccion').value.trim();
    const password = document.getElementById('password').value;
    const password2 = document.getElementById('password2').value;
    const errorMensaje = document.getElementById('errorMensaje');

    errorMensaje.innerText = "";
    errorMensaje.style.display = "none";

    // Validación: tipo de usuario
    if (tipoUsuario === "") {
        errorMensaje.innerText = "Debes seleccionar un tipo de usuario.";
        errorMensaje.style.display = "block";
        return;
    }

    // Validación: edad mínima
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
        return;
    }

    // Validación: formato de correo
    const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regexCorreo.test(correo)) {
        errorMensaje.innerText = "Por favor, ingresa un correo electrónico válido.";
        errorMensaje.style.display = "block";
        return;
    }

    // Validación: contraseña segura
    const regexPassword = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{6,18}$/;
    if (!regexPassword.test(password)) {
        errorMensaje.innerHTML = "La contraseña debe contener al menos:<ul><li>Entre 6 y 18 caracteres</li><li>1 número</li><li>1 letra mayúscula</li><li>1 carácter especial</li></ul>";
        errorMensaje.style.display = "block";
        return;
    }

    // Validación: confirmación de contraseña
    if (password !== password2) {
        errorMensaje.innerText = "Las contraseñas no coinciden.";
        errorMensaje.style.display = "block";
        return;
    }

    // Verificar si el nombre de usuario ya está registrado
    let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];

    if (usuarios.some(usuario => usuario.nombreUsuario === nombreUsuario)) {
        alert("El nombre de usuario ya está registrado.");
        return;
    }

    // Crear objeto usuario
    const usuario = {
        nombreUsuario,
        nombreCompleto,
        fechaNacimiento,
        correo,
        direccion,
        password,
        role: tipoUsuario 
    };

    // Guardar en localStorage
    usuarios.push(usuario);
    localStorage.setItem("usuarios", JSON.stringify(usuarios));
    localStorage.setItem("usuario", nombreUsuario);

    alert("Usuario registrado correctamente.");

    const usuarioActivo = JSON.parse(localStorage.getItem("usuarioActivo"));

    // Redirigir según tipo de usuario activo
    if (usuarioActivo && usuarioActivo.role === 'administrador') {
        window.location.href = "../user/usuarios.html";
    } else {
        window.location.href = "./inicio_sesion.html";
    }
});