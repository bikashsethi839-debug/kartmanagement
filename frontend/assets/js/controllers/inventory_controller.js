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

  document.addEventListener('DOMContentLoaded', ()=>{
    const form = getEl('#inventory-form');
    const clearBtn = getEl('#clear-form');

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

    // live updates
    form.addEventListener('input', ()=>{
      const data = readForm(form);
      renderPreview(data);
    });

    // clear
    clearBtn.addEventListener('click', ()=>{
      form.reset();
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
          alert('Product created!');
          // reset original state to new created product for undo
          originalState.name = payload.name;
          originalState.sku = payload.sku;
          originalState.price = payload.price;
          originalState.stock = payload.stock;
          originalState.description = payload.description;
          form.reset();
          renderPreview(readForm(form));
        }else{
          alert('Failed to create product');
        }
      }catch(err){
        console.error(err);
        alert('Network error');
      }
    });
  });
})();
