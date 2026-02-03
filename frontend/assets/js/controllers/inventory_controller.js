(function(){
  function getEl(selector){ return document.querySelector(selector); }

  function readForm(form){
    return {
      name: form.querySelector('[name="name"]').value || '',
      sku: form.querySelector('[name="sku"]').value || '',
      price: parseFloat(form.querySelector('[name="price"]').value || 0) || 0,
      stock: parseInt(form.querySelector('[name="stock"]').value || 0) || 0,
      description: form.querySelector('[name="description"]').value || ''
    };
  }

  function renderPreview(data){
    const el = getEl('#live-preview');
    el.innerHTML = `<div class="card">
      <h3>${data.name || 'Product name'}</h3>
      <p>SKU: ${data.sku || '-'}</p>
      <p>Price: $${(data.price || 0).toFixed(2)}</p>
      <p>Stock: ${data.stock || 0}</p>
      <p>${data.description || ''}</p>
    </div>`;
  }

  async function createProduct(payload){
    const res = await fetch('/api/products', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
    });
    return res.json();
  }

  document.addEventListener('DOMContentLoaded', async ()=>{
    const form = getEl('#inventory-form');
    const clearBtn = getEl('#clear-form');
    const select = getEl('#product-select');
    const loadBtn = getEl('#load-selected');
    const updateBtn = getEl('#update-btn');
    const deleteBtn = getEl('#delete-btn');
    const createBtn = getEl('#create-btn');

    let editingId = null;

    // add undo button
    const undoBtn = document.createElement('button');
    undoBtn.type = 'button';
    undoBtn.id = 'undo-form';
    undoBtn.textContent = 'Undo';
    form.appendChild(undoBtn);

    // capture initial state
    const originalState = readForm(form);

    // initial render
    renderPreview(originalState);

    // populate products select
    async function loadProducts(){
      const r = await fetch('/api/products');
      const data = (await r.json()).data || [];
      select.innerHTML = '<option value="">-- New Product --</option>' + data.map(p=>`<option value="${p.id}">${p.id} - ${p.name}</option>`).join('');
    }

    await loadProducts();

    loadBtn.addEventListener('click', async ()=>{
      const id = select.value;
      if(!id) return; // nothing
      const r = await fetch(`/api/products/${id}`);
      const data = (await r.json()).data;
      form.querySelector('[name="name"]').value = data.name; form.querySelector('[name="sku"]').value = data.sku; form.querySelector('[name="price"]').value = data.price; form.querySelector('[name="stock"]').value = data.stock; form.querySelector('[name="description"]').value = data.description;
      editingId = id; createBtn.style.display='none'; updateBtn.style.display='inline-block'; deleteBtn.style.display='inline-block';
      renderPreview(readForm(form));
    });

    // live updates
    form.addEventListener('input', ()=>{
      const data = readForm(form);
      renderPreview(data);
    });

    // clear
    clearBtn.addEventListener('click', ()=>{
      form.reset();
      editingId = null; createBtn.style.display='inline-block'; updateBtn.style.display='none'; deleteBtn.style.display='none';
      renderPreview(readForm(form));
    });

    // undo
    undoBtn.addEventListener('click', ()=>{
      form.querySelector('[name="name"]').value = originalState.name;
      form.querySelector('[name="sku"]').value = originalState.sku;
      form.querySelector('[name="price"]').value = originalState.price;
      form.querySelector('[name="stock"]').value = originalState.stock;
      form.querySelector('[name="description"]').value = originalState.description;
      renderPreview(readForm(form));
    });

    // submit => create
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const payload = readForm(form);
      try{
        const resp = await createProduct(payload);
        if(resp && resp.status === 'created'){
          if(window.UI) window.UI.toast('Product created'); else alert('Product created!');
          // refresh select
          await loadProducts();
          form.reset();
          renderPreview(readForm(form));
        }else{
          if(window.UI) window.UI.toast('Failed to create'); else alert('Failed to create product');
        }
      }catch(err){
        console.error(err);
        if(window.UI) window.UI.toast('Network error'); else alert('Network error');
      }
    });

    updateBtn.addEventListener('click', async ()=>{
      if(!editingId) return;
      const payload = readForm(form);
      const r = await fetch(`/api/products/${editingId}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
      if(r.ok){ if(window.UI) window.UI.toast('Saved'); await loadProducts(); } else { if(window.UI) window.UI.toast('Save failed'); }
    });

    deleteBtn.addEventListener('click', async ()=>{
      if(!editingId) return;
      const ok = window.UI ? await window.UI.confirm('Delete product?') : confirm('Delete?');
      if(!ok) return;
      const r = await fetch(`/api/products/${editingId}`, {method:'DELETE'});
      if(r.ok){ if(window.UI) window.UI.toast('Deleted'); form.reset(); editingId=null; await loadProducts(); renderPreview(readForm(form)); }
    });

  });
})();
