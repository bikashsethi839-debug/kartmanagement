(async function(){
  async function fetchCart(){
    const res = await window.fetchJSON('/api/cart');
    return res.data || [];
  }

  async function render(){
    const items = await fetchCart();
    const container = document.getElementById('cart-items');
    container.innerHTML = '';
    if(items.length === 0){
      container.innerHTML = '<p>Your cart is empty.</p>';
      return;
    }

    const list = document.createElement('div');
    list.className = 'grid';
    items.forEach(it => {
      const el = document.createElement('div');
      el.className = 'card';
      el.innerHTML = `<h3>${it.name}</h3>
        <p>Price: $${it.price}</p>
        <p>Quantity: <button class="qty-decrease">-</button> <span class="qty">${it.quantity}</span> <button class="qty-increase">+</button></p>
        <p><a href="#" class="remove">Remove</a></p>`;

      el.querySelector('.qty-increase').addEventListener('click', async ()=>{
        await fetch(`/api/cart/${it.id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify({quantity: it.quantity + 1})});
        render();
      });

      el.querySelector('.qty-decrease').addEventListener('click', async ()=>{
        const newQty = Math.max(1, it.quantity -1);
        await fetch(`/api/cart/${it.id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify({quantity: newQty})});
        render();
      });

      el.querySelector('.remove').addEventListener('click', async (e)=>{
        e.preventDefault();
        await fetch(`/api/cart/${it.id}`, {method:'DELETE'});
        render();
      });

      list.appendChild(el);
    });

    // Clear cart button
    const clearBtn = document.createElement('button');
    clearBtn.textContent = 'Clear Cart';
    clearBtn.addEventListener('click', async ()=>{
      // delete each item
      for(const it of items){
        await fetch(`/api/cart/${it.id}`, {method:'DELETE'});
      }
      render();
    });

    container.appendChild(list);
    container.appendChild(clearBtn);
  }

  // init
  document.addEventListener('DOMContentLoaded', ()=>{
    render();
  });
})();
