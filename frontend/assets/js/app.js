// Minimal frontend boot file
console.log('App loaded');

// Simple helper to fetch json
async function fetchJSON(url, opts){
  const res = await fetch(url, opts);
  return res.json();
}

window.fetchJSON = fetchJSON; // expose for controllers
