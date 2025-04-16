document.querySelectorAll(".add-to-cart").forEach(button => {
    button.addEventListener("click", () => {
        const name = button.getAttribute("data-game");
        const price = parseInt(button.getAttribute("data-price"));

        let cart = JSON.parse(localStorage.getItem("cart")) || [];

        const existingProduct = cart.find(p => p.name === name);
        if (existingProduct) {
            existingProduct.quantity++;
        } else {
            cart.push({ name, price, quantity: 1 });
        }

        localStorage.setItem("cart", JSON.stringify(cart));

        alert(`${name} agregado al carrito!`);
    });
});


function loadCart() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let cartItemsContainer = document.getElementById("cart-items");
    let subtotalElement = document.getElementById("subtotal");
    let totalElement = document.getElementById("total");

    cartItemsContainer.innerHTML = ""; // Limpiar la lista antes de actualizar
    let subtotal = 0;

    cart.forEach(product => {
        let item = document.createElement("div");
        item.classList.add("d-flex", "justify-content-between", "w-100", "px-3", "mb-2", "align-items-center");

        item.innerHTML = `
            <p class="text-center w-25">${product.name}</p>
            <p class="text-center w-25">$${product.price}</p>
            <p class="text-center w-25">${product.quantity}</p>
            <button class="remove-item" data-name="${product.name}"> ❌ </button>
        `;

        cartItemsContainer.appendChild(item);
        subtotal += product.price * product.quantity;
    });

    subtotalElement.innerText = `Subtotal: $${subtotal}`;
    totalElement.innerText = `Total: $${subtotal}`;

    // Agregar eventos para eliminar productos
    document.querySelectorAll(".remove-item").forEach(button => {
        button.addEventListener("click", () => {
            removeFromCart(button.getAttribute("data-name"));
        });
    });
}

function removeFromCart(name) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart = cart.filter(product => product.name !== name); 
    localStorage.setItem("cart", JSON.stringify(cart));
    loadCart(); // Recargamos el carrito
}

document.addEventListener("DOMContentLoaded", loadCart);



document.getElementById("checkout-btn").addEventListener("click", function () {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    if (cart.length === 0) {
        alert("El carrito está vacío. Agrega productos antes de pagar.");
        return;
    }

    // Guardar la compra en LocalStorage
    localStorage.setItem("lastPurchase", JSON.stringify(cart));

    // Vaciar el carrito en LocalStorage
    localStorage.removeItem("cart");

    // Limpiar los elementos visibles del carrito
    document.getElementById("cart-items").innerHTML = "";
    document.getElementById("subtotal").innerText = "Subtotal: $0";
    document.getElementById("total").innerText = "Total: $0";

    // Mostrar mensaje de éxito
    alert("Pago realizado con éxito. ¡Gracias por tu compra!");
});
