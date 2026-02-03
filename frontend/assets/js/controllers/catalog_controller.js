(async function(){
  try{
    const resp = await window.fetchJSON('/api/products');
    const container = document.getElementById('products');
    resp.data.forEach(p => {
      const el = document.createElement('div');
      el.className = 'card';
      el.innerHTML = `<h3>${p.name}</h3><p>$${p.price}</p><p>${p.description || ''}</p><button data-id="${p.id}">Add to cart</button>`;
      el.querySelector('button').addEventListener('click', async (e)=>{
        await fetch('/api/cart', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({product_id:p.id, quantity:1})});
        alert('Added to cart');
      });
      container.appendChild(el);
    });
  }catch(e){
    console.error(e);
  }
})();
