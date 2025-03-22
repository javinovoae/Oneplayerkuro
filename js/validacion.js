document.getElementById('formulario').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío automático del formulario

    //esto trae la info puesta en id del html 
    const password = document.getElementById('password').value;
    const password2 = document.getElementById('password2').value;
    const errorMensaje = document.getElementById('errorMensaje');

    errorMensaje.innerText = "";
    errorMensaje.style.display = "none";


    // Expresión regular de la contraseña
    const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{6,18}$/;
    if (!regex.test(password)) {
        errorMensaje.innerText = "La contraseña debe tener entre 6 y 18 caracteres, incluir al menos un número, una letra mayúscula y un carácter especial.";
        errorMensaje.style.display = "block";
        return;
    }

    // Validar que las contraseñas coincidan
    if (password !== password2) {
        errorMensaje.innerText = "Las contraseñas no coinciden.";
        errorMensaje.style.display = "block";
        return;
    }
      // ocultar el mensaje de error
        errorMensaje.innerText = "";
        errorMensaje.style.display = "none";
    
      // Deshabilitar botón de envío para evitar doble clic
        document.querySelector('.btn-registro').disabled = true;
    
      // Enviar formulario
        alert("Formulario enviado correctamente.");
        this.submit();
        
        //para recargar la pagina y no se caiga
        setTimeout(() => {
            location.reload();  
        }, 1000);

    });