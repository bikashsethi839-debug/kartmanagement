(async function(){
  function q(s){return document.querySelector(s)}
  function getParam(name){
    return new URLSearchParams(window.location.search).get(name);
  }

  async function fetchProducts(){
    const r = await fetch('/api/products');
    return (await r.json()).data || [];
  }

  async function load(){
    let id = getParam('id');
    if(!id){
      const all = await fetchProducts();
      if(all.length===0){ document.getElementById('product-detail').innerHTML = '<p>No products</p>'; return; }
      id = all[0].id;
    }
    const r = await fetch(`/api/products/${id}`);
    if(!r.ok){ document.getElementById('product-detail').innerHTML = '<p>Not found</p>'; return; }
    const data = (await r.json()).data;

    q('#product-detail').innerHTML = `
      <div class="card">
        <h2>Editing: <input id="p-name" value="${data.name||''}" /></h2>
        <p>SKU: <input id="p-sku" value="${data.sku||''}" /></p>
        <p>Price: <input id="p-price" type="number" step="0.01" value="${data.price||0}" /></p>
        <p>Stock: <input id="p-stock" type="number" value="${data.stock||0}" /></p>
        <p>Description:<br/><textarea id="p-desc">${data.description||''}</textarea></p>
        <p><button id="save-product">Save</button> <button id="danger-delete" style="background:#b91c1c">Danger Zone: Delete</button></p>
        <hr />
        <h3>Reviews</h3>
        <div id="reviews-list"></div>
        <form id="review-form">
          <input name="author" placeholder="Your name" /><br/>
          <input name="rating" type="number" min="1" max="5" placeholder="Rating" /><br/>
          <textarea name="comment" placeholder="Comment"></textarea><br/>
          <button type="submit">Add Review</button>
        </form>
      </div>`;

    q('#save-product').addEventListener('click', async ()=>{
      const payload = {
        name: q('#p-name').value,
        sku: q('#p-sku').value,
        price: parseFloat(q('#p-price').value||0),
        stock: parseInt(q('#p-stock').value||0),
        description: q('#p-desc').value
      };
      const resp = await fetch(`/api/products/${id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
      if(resp.ok){ alert('Saved'); } else { alert('Save failed'); }
    });

    q('#danger-delete').addEventListener('click', async ()=>{
      if(!confirm('Permanently delete this product?')) return;
      const resp = await fetch(`/api/products/${id}`, {method:'DELETE'});
      if(resp.ok){ window.location.href='/catalog.html'; }
      else alert('Delete failed');
    });

    // reviews
    async function loadReviews(){
      const r = await fetch(`/api/products/${id}/reviews`);
      const json = await r.json();
      const list = json.data || [];
      const el = q('#reviews-list');
      el.innerHTML = list.map(rv=>`<div class="card"><strong>${rv.author}</strong> (${rv.rating})<p>${rv.comment||''}</p></div>`).join('') || '<p>No reviews</p>';
    }

    loadReviews();

    q('#review-form').addEventListener('submit', async (e)=>{
      e.preventDefault();
      const form = e.target;
      const payload = {author: form.author.value||'Anon', rating: parseInt(form.rating.value||5), comment: form.comment.value};
      const r = await fetch(`/api/products/${id}/reviews`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
      if(r.ok){ alert('Review added'); form.reset(); loadReviews(); }
      else alert('Failed');
    });
  }

  document.addEventListener('DOMContentLoaded', ()=>{ load(); });
})();
