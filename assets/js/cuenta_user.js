const usuarioLogueado = JSON.parse(localStorage.getItem("usuarioActivo"));

if (usuarioLogueado) {
    // Rellenar campos
    document.getElementById('cuenta_nombre_completo').value = usuarioLogueado.nombreCompleto;
    document.getElementById('cuenta_correo').value = usuarioLogueado.correo;
    document.getElementById('cuenta_direccion').value = usuarioLogueado.direccion;
    document.getElementById('cuenta_fecha_nac').value = usuarioLogueado.fechaNacimiento;
    
    // Mostrar mensaje de bienvenida con el usuario 
    const mensajeBienvenida = document.getElementById('mensaje_bienvenida');
    if (mensajeBienvenida) {
        mensajeBienvenida.innerHTML = `Bienvenid@ ${usuarioLogueado.nombreUsuario}`;
    }
} else {
    alert("Debes iniciar sesión en la página");
    window.location.href = "../auth/form_registro.html";
}

function editarCuenta() {
    // Activar edición
    document.getElementById("cuenta_nombre_completo").disabled = false;
    document.getElementById("cuenta_fecha_nac").disabled = false;
    document.getElementById("cuenta_correo").disabled = false;
    document.getElementById("cuenta_direccion").disabled = false;

    const boton = document.querySelector(".btn-edit button");
    boton.textContent = "Guardar";
    boton.setAttribute("onclick", "guardarCuenta()");
}

function guardarCuenta() {
    const usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];
    const usuarioIndex = usuarios.findIndex(u => u.nombreUsuario === usuarioLogueado.nombreUsuario);

    // Obtener nuevos valores
    const nombreCompleto = document.getElementById("cuenta_nombre_completo").value;
    const fechaNacimiento = document.getElementById("cuenta_fecha_nac").value;
    const correo = document.getElementById("cuenta_correo").value;
    const direccion = document.getElementById("cuenta_direccion").value;

    // Actualizar datos
    usuarios[usuarioIndex] = {
        ...usuarios[usuarioIndex],
        nombreCompleto,
        fechaNacimiento,
        correo,
        direccion
    };

    localStorage.setItem("usuarios", JSON.stringify(usuarios));

    localStorage.setItem("usuarioActivo", JSON.stringify(usuarios[usuarioIndex]));

    alert("¡Usuario editado con éxito!");

    document.getElementById("cuenta_nombre_completo").disabled = true;
    document.getElementById("cuenta_fecha_nac").disabled = true;
    document.getElementById("cuenta_correo").disabled = true;
    document.getElementById("cuenta_direccion").disabled = true;

    const boton = document.querySelector(".btn-edit button");
    boton.textContent = "Editar";
    boton.setAttribute("onclick", "editarCuenta()");
}