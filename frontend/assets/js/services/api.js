const API_BASE = '/api';

export async function getProducts(){
  return window.fetchJSON(`${API_BASE}/products`);
}

export async function getProduct(id){
  return window.fetchJSON(`${API_BASE}/products/${id}`);
}

export async function createProduct(payload){
  return window.fetchJSON(`${API_BASE}/products`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
}

export async function addToCart(payload){
  return window.fetchJSON(`${API_BASE}/cart`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
}

export async function getCart(){
  return window.fetchJSON(`${API_BASE}/cart`);
}
