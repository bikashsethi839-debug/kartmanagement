(async function(){
  const API = '/api/products';

  function el(selector){return document.querySelector(selector)}

  async function fetchProducts(){
    const resp = await fetch(API);
    const json = await resp.json();
    return json.data || [];
  }

  function createCellInput(value){
    const input = document.createElement('input');
    input.value = value === null || value === undefined ? '' : value;
    input.style.width = '100%';
    return input;
  }

  async function render(){
    const products = await fetchProducts();
    const container = el('#dashboard-table');
    container.innerHTML = '';

    const toolbar = document.createElement('div');
    const bulkDeleteBtn = document.createElement('button');
    bulkDeleteBtn.textContent = 'Delete Selected';
    toolbar.appendChild(bulkDeleteBtn);
    container.appendChild(toolbar);

    const table = document.createElement('table');
    table.style.width='100%';
    table.style.borderCollapse='collapse';
    table.innerHTML = `<thead><tr><th></th><th>ID</th><th>Name</th><th>SKU</th><th>Price</th><th>Stock</th><th>Actions</th></tr></thead>`;
    const tbody = document.createElement('tbody');

    for(const p of products){
      const tr = document.createElement('tr');
      tr.style.borderTop='1px solid #233';
      const checkboxTd = document.createElement('td');
      checkboxTd.innerHTML = `<input type="checkbox" data-id="${p.id}" />`;
      tr.appendChild(checkboxTd);

      tr.appendChild(Object.assign(document.createElement('td'), {textContent: p.id}));

      const nameTd = document.createElement('td');
      nameTd.textContent = p.name;
      nameTd.addEventListener('click', ()=>{ startEditing(nameTd, 'name', p); });
      tr.appendChild(nameTd);

      const skuTd = document.createElement('td');
      skuTd.textContent = p.sku || '';
      skuTd.addEventListener('click', ()=>{ startEditing(skuTd, 'sku', p); });
      tr.appendChild(skuTd);

      const priceTd = document.createElement('td');
      priceTd.textContent = p.price;
      priceTd.addEventListener('click', ()=>{ startEditing(priceTd, 'price', p, 'number'); });
      tr.appendChild(priceTd);

      const stockTd = document.createElement('td');
      stockTd.textContent = p.stock;
      stockTd.addEventListener('click', ()=>{ startEditing(stockTd, 'stock', p, 'number'); });
      tr.appendChild(stockTd);

      const actionsTd = document.createElement('td');
      const dupBtn = document.createElement('button'); dupBtn.textContent='Duplicate';
      dupBtn.addEventListener('click', async ()=>{
        await fetch(`${API}/${p.id}/duplicate`, {method:'POST'});
        render();
      });
      const delBtn = document.createElement('button'); delBtn.textContent='Delete';
      delBtn.style.marginLeft='6px';
      delBtn.addEventListener('click', async ()=>{
        if(confirm('Delete this product?')){
          await fetch(`${API}/${p.id}`, {method:'DELETE'});
          render();
        }
      });
      const gotoDetail = document.createElement('button'); gotoDetail.textContent='Open'; gotoDetail.style.marginLeft='6px';
      gotoDetail.addEventListener('click', ()=>{ window.location.href = `/product.html?id=${p.id}` });
      actionsTd.appendChild(dupBtn); actionsTd.appendChild(delBtn); actionsTd.appendChild(gotoDetail);
      tr.appendChild(actionsTd);

      tbody.appendChild(tr);
    }

    table.appendChild(tbody);
    container.appendChild(table);

    bulkDeleteBtn.addEventListener('click', async ()=>{
      const checked = Array.from(container.querySelectorAll('input[type=checkbox]:checked')).map(i=>parseInt(i.getAttribute('data-id')));
      if(checked.length===0){ alert('Select at least one'); return; }
      if(!confirm('Delete selected products?')) return;
      await fetch('/api/products/bulk-delete', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ids:checked})});
      render();
    });

    // inline editing helper
    function startEditing(td, field, product, type='text'){
      const current = product[field];
      td.innerHTML = '';
      const input = createCellInput(current);
      if(type==='number') input.type='number';
      td.appendChild(input);
      input.focus();
      const save = async ()=>{
        const val = (type==='number') ? (input.value===''?0:parseFloat(input.value)) : input.value;
        const payload = Object.assign({}, product, {[field]: val});
        const res = await fetch(`${API}/${product.id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
        if(res.ok){ render(); } else { alert('Save failed'); }
      };
      input.addEventListener('blur', save);
      input.addEventListener('keydown', (e)=>{ if(e.key==='Enter') input.blur(); });
    }
  }

  document.addEventListener('DOMContentLoaded', ()=>{ render(); });
})();
