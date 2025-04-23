const cart = JSON.parse(localStorage.getItem('cart')) || [];


function saveCart() {
  localStorage.setItem('cart', JSON.stringify(cart));
}


function addToCart(name, price) {
  const existing = cart.find(item => item.name === name);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ name, price, qty: 1 });
  }
  saveCart();
  alert(`${name} added to cart!`);
}


function goToProduct(name) {
  window.location.href = 'product.html'; 
}

function goToProduct1(name) {
  window.location.href = 'product2.html'; 
}

function goToProduct2(name) {
  window.location.href = 'product3.html'; 
}

function goToProduct3(name) {
  window.location.href = 'product4.html'; 
}

function goToProduct4(name) {
  window.location.href = 'product5.html'; 
}

function goToProduct5(name) {
  window.location.href = 'product6.html'; 
}

function goToProduct6(name) {
  window.location.href = 'product7.html'; 
}

function goToProduct7(name) {
  window.location.href = 'product8.html'; 
}

function goToProduct8(name) {
  window.location.href = 'product9.html';
}

function renderCart() {
  const container = document.getElementById('cart-items');
  const totalDisplay = document.getElementById('cart-total');
  if (!container || !totalDisplay) return;


  container.innerHTML = '';
  let total = 0;


  cart.forEach((item, index) => {
    const itemDiv = document.createElement('div');
    const itemTotal = (item.price * item.qty).toFixed(2);
    total += parseFloat(itemTotal);


    itemDiv.innerHTML = `
      <p><strong>${item.name}</strong><br>Quantity: ${item.qty}<br>Price: $${itemTotal}</p>
      <button onclick="removeItem(${index})">Delete</button>
    `;
    container.appendChild(itemDiv);
  });


  totalDisplay.textContent = total.toFixed(2);
}


function removeItem(index) {
  cart.splice(index, 1);
  saveCart();
  renderCart();
}


function clearCart() {
  cart.length = 0;
  saveCart();
  renderCart();
}


if (window.location.pathname.includes('cart.html')) {
  renderCart();
}


if (window.location.pathname.includes('thankyou.html')) {
  const summary = document.getElementById('order-summary');
  let total = 0;
  summary.innerHTML = '<ul>' + cart.map(item => {
    total += item.price * item.qty;
    return `<li>${item.name} (${item.qty}): $${(item.price * item.qty).toFixed(2)}</li>`;
  }).join('') + `</ul><p>Order Total: $${total.toFixed(2)}</p>`;
  clearCart();
}


const checkoutForm = document.getElementById('checkout-form');
if (checkoutForm) {
  checkoutForm.addEventListener('submit', e => {
    e.preventDefault();
    window.location.href = 'thankyou.html';
  });
}
