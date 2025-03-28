document.addEventListener("DOMContentLoaded", function () {
    const usuarioLogueado = JSON.parse(localStorage.getItem("usuarioActivo"));

    const navRegister = document.getElementById('nav-register');
    const navLogin = document.getElementById('nav-login');
    const navAccount = document.getElementById('nav-account');
    const navCart = document.getElementById('nav-cart');
    const navLogout = document.getElementById('nav-logout');

    if (usuarioLogueado) {
        navRegister.style.display = "none";
        navLogin.style.display = "none";
        navAccount.style.display = "block";
        navCart.style.display = "block";
        navLogout.style.display = "block";
    } else {
        navRegister.style.display = "block";
        navLogin.style.display = "block";
        navAccount.style.display = "none";
        navCart.style.display = "none";
        navLogout.style.display = "none";
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

