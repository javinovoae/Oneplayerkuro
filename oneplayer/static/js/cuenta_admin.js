document.addEventListener('DOMContentLoaded', function () {

    let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
    console.log("Usuarios cargados desde localStorage:", usuarios);

    const usuarioLogueado = JSON.parse(localStorage.getItem('usuarioActivo'));
    console.log("Usuario logueado:", usuarioLogueado);

    if (!usuarioLogueado || usuarioLogueado.role !== "admin") {
        alert("No tienes permisos para acceder a esta página.");
        window.location.href = "../auth/inicio_sesion.html"; 
        return;
    }

    if (usuarios.length > 0) {
        mostrarUsuarios(usuarios);
    } else {
        alert("No hay usuarios registrados.");
        document.getElementById('lista_usuarios').innerHTML = "<p>No hay usuarios registrados para mostrar.</p>";
    }

    function mostrarUsuarios(usuarios) {
        console.log("Mostrando usuarios:", usuarios); 
        const listaUsuarios = document.getElementById("lista_usuarios");
        listaUsuarios.innerHTML = "";
        usuarios.forEach(usuario => {
            const divUsuario = document.createElement("div");
            divUsuario.classList.add("usuario-item", "mt-3", "border", "p-3");

            divUsuario.innerHTML = `
                <p><strong>Nombre:</strong> ${usuario.nombreUsuario}</p>
                <p><strong>Correo:</strong> ${usuario.correo}</p>
                <button onclick="editarUsuario('${usuario.nombreUsuario}')" class="btn btn-info btn-sm">Editar</button>
                <button onclick="cambiarContraseñaUsuario('${usuario.nombreUsuario}')" class="btn btn-warning btn-sm ml-2">Cambiar Contraseña</button>
                <button onclick="eliminarUsuario('${usuario.nombreUsuario}')" class="btn btn-danger btn-sm ml-2">Eliminar</button>
            `;

            listaUsuarios.appendChild(divUsuario);
        });
    }

    window.cambiarContraseñaUsuario = function (nombreUsuario) {
        const usuarios = JSON.parse(localStorage.getItem("usuarios"));
        const usuarioIndex = usuarios.findIndex(usuario => usuario.nombreUsuario === nombreUsuario);

        if (usuarioIndex !== -1) {
            const passwordNuevo = prompt("Introduce la nueva contraseña para el usuario:");

            if (validarContraseña(passwordNuevo)) {
                usuarios[usuarioIndex].password = passwordNuevo;
                localStorage.setItem("usuarios", JSON.stringify(usuarios));

                alert("Contraseña cambiada con éxito.");
                mostrarUsuarios(usuarios); 
            } else {
                alert("La contraseña no cumple con los requisitos de seguridad.");
            }
        }
    };

    function validarContraseña(password) {
        const longitudMinima = 8;
        const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;

        if (password.length < longitudMinima) {
            alert("La contraseña debe tener al menos 8 caracteres.");
            return false;
        }

        if (!regex.test(password)) {
            alert("La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.");
            return false;
        }

        return true;
    }

    window.eliminarUsuario = function (nombreUsuario) {
        const usuarios = JSON.parse(localStorage.getItem("usuarios"));
        const usuariosActualizados = usuarios.filter(usuario => usuario.nombreUsuario !== nombreUsuario);

        const confirmar = confirm(`¿Estás seguro de que quieres eliminar al usuario ${nombreUsuario}?`);
        if (confirmar) {
            localStorage.setItem("usuarios", JSON.stringify(usuariosActualizados));
            alert("Usuario eliminado con éxito.");
            mostrarUsuarios(usuariosActualizados);
        }
    };
});



