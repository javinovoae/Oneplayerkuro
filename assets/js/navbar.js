document.addEventListener("DOMContentLoaded", function () {
    const usuarioLogueado = JSON.parse(localStorage.getItem("usuarioActivo"));

    // Elementos del navbar
    const navRegister = document.getElementById('nav-register');
    const navLogin = document.getElementById('nav-login');
    const navAccount = document.getElementById('nav-account');
    const navCart = document.getElementById('nav-cart');
    const navLogout = document.getElementById('nav-logout');
    const navGestion = document.getElementById('nav-gestion');

    // Si hay un usuario logueado
    if (usuarioLogueado) {
        // Ocultar elementos de registro y login
        navRegister.style.display = "none";
        navLogin.style.display = "none";
        navAccount.style.display = "block";
        navLogout.style.display = "block";

        // Mostrar carrito solo si el usuario es un cliente
        navCart.style.display = usuarioLogueado.tipo_usuario === "cliente" ? "block" : "none";

        // Mostrar opciones de gestión solo si el usuario es un administrador
        navGestion.style.display = usuarioLogueado.tipo_usuario === "administrador" ? "block" : "none";
    } else {
        // Si no hay usuario logueado, mostrar registro y login
        navRegister.style.display = "block";
        navLogin.style.display = "block";
        navAccount.style.display = "none";
        navCart.style.display = "none";
        navLogout.style.display = "none";
        navGestion.style.display = "none";
    }

    // Logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function () {
            localStorage.removeItem("usuarioActivo");
            window.location.reload();  
        });
    }
});

