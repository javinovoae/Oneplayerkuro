
document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const isLogged = urlParams.get('logged') === 'true' || localStorage.getItem("usuarioActivo");

    // Obtener los elementos del navbar
    const navRegister = document.getElementById('nav-register');
    const navLogin = document.getElementById('nav-login');
    const navAccount = document.getElementById('nav-account');
    const navCart = document.getElementById('nav-cart');
    const navLogout = document.getElementById('nav-logout');

    // Mostrar u ocultar opciones del navbar según el estado de la sesión
    if (isLogged) {
        // Mostrar opciones para usuarios logueados
        navRegister.style.display = "none";
        navLogin.style.display = "none";
        navAccount.style.display = "block";
        navCart.style.display = "block";
        navLogout.style.display = "block";
    } else {
        // Mostrar opciones para usuarios no logueados
        navRegister.style.display = "block";
        navLogin.style.display = "block";
        navAccount.style.display = "none";
        navCart.style.display = "none";
        navLogout.style.display = "none";
    }
});

