(async function(){
  try{
    const resp = await window.fetchJSON('/api/products');
    const container = document.getElementById('products');
    resp.data.forEach(p => {
      const el = document.createElement('div');
      el.className = 'card';
      el.innerHTML = `<h3>${p.name}</h3><p class="small-muted">SKU: ${p.sku || '-'}</p><p>$${p.price}</p><p>${p.description || ''}</p>
        <div style="display:flex;gap:8px;margin-top:8px"><button data-id="${p.id}" class="add">Add to cart</button><button class="quick">Quick View</button><button class="del" style="background:transparent;color:var(--danger);border:1px solid rgba(255,255,255,0.04)">Delete</button></div>`;

      el.querySelector('.add').addEventListener('click', async (e)=>{
        await fetch('/api/cart', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({product_id:p.id, quantity:1})});
        if(window.UI) window.UI.toast('Added to cart'); else alert('Added to cart');
      });

      el.querySelector('.del').addEventListener('click', async ()=>{
        if(window.UI){
          const ok = await window.UI.confirm('Delete this product?');
          if(!ok) return;
        } else if(!confirm('Delete?')) return;
        await fetch(`/api/products/${p.id}`, {method:'DELETE'});
        if(window.UI) window.UI.toast('Deleted');
        el.remove();
      });

      el.querySelector('.quick').addEventListener('click', ()=>{
        // build quick view modal
        const html = `<div style="display:flex;gap:12px;align-items:flex-start"><div style="flex:1"><h2>${p.name}</h2><p class="small-muted">SKU: ${p.sku || '-'}</p><p>$${p.price}</p><p>${p.description || ''}</p>
          <p>Quantity: <input id="quick-qty" type="number" value="1" min="1" style="width:80px" /></p></div>
          <div style="width:220px"><h4>Quick Edit</h4><input id="quick-name" placeholder="Name" value="${p.name}" /><input id="quick-price" type="number" step="0.01" value="${p.price}" /><textarea id="quick-desc">${p.description||''}</textarea></div></div>`;
        window.UI.show({html, buttons:[{text:'Add to cart', className:'btn-ok', onClick:async ()=>{ const qty = parseInt(document.getElementById('quick-qty').value||1); await fetch('/api/cart', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({product_id:p.id, quantity:qty})}); window.UI.toast('Added');}},{text:'Save changes', className:'btn-ok', onClick:async ()=>{ const payload={name:document.getElementById('quick-name').value, price:parseFloat(document.getElementById('quick-price').value||0), description:document.getElementById('quick-desc').value}; const r = await fetch(`/api/products/${p.id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)}); if(r.ok){ window.UI.toast('Saved'); } else { window.UI.toast('Save failed'); } }},{text:'Close', className:'btn-cancel'}]});
      });

      container.appendChild(el);
    });
  }catch(e){
    console.error(e);
  }
})();
