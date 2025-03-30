document.addEventListener('DOMContentLoaded', function() {
    let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
    console.log(usuarios);

    //Usuarios por defecto en localStorage
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

        const usuarioPrueba1 = {
            nombreUsuario: 'Prueba1',
            password: 'test123', 
            nombreCompleto: 'Esteban Hernández Rodríguez',
            fechaNacimiento: '15-07-1990',
            correo: 'esteban@prueba1.com', 
            role: 'usuario', 
            direccionEnvio: 'Calle Nueva 123, Depto. 890, Comuna, Ciudad' 
        };
        usuarios.push(usuarioPrueba1);

        const usuarioPrueba2 = {
            nombreUsuario: 'Prueba2',
            password: 'test456', 
            nombreCompleto: 'Ettielë Ynnocent',
            fechaNacimiento: '22-09-1995',
            correo: 'ettiele@prueba2.com', 
            role: 'usuario'
        };
        usuarios.push(usuarioPrueba2);

        localStorage.setItem('usuarios', JSON.stringify(usuarios));
    }

    //Formulario
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

        const usuarioEncontrado = usuarios.find(usuario => usuario.nombreUsuario === nombreUsuario && usuario.password === passwordIngresado);

        if (!usuarioEncontrado) {
            errorMensaje.innerText = 'Nombre de usuario o contraseña incorrectos.';
            errorMensaje.style.display = "block";
            return;
        }

        //Usuario activo en localStorage
        localStorage.setItem('usuarioActivo', JSON.stringify(usuarioEncontrado));

        alert('Inicio de sesión exitoso. ¡Bienvenid@ ' + usuarioEncontrado.nombreUsuario + '!');

        // Redirección basada en el rol
        if (usuarioEncontrado.role === "admin") {
            window.location.href = "../user/usuarios.html";
        } else {
            window.location.href = "../user/cuenta.html"; 
        }
    });

    //Mensaje de error
    function crearErrorMensaje() {
        const errorDiv = document.createElement("div");
        errorDiv.id = 'errorMensaje';
        errorDiv.style.color = 'red';
        errorDiv.style.marginTop = '10px';
        document.getElementById('inicio_sesion').appendChild(errorDiv);
        return errorDiv;
    }
});
