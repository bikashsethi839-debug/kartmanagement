// Minimal frontend boot file
console.log('App loaded');

// UI utilities available at window.UI (modal / confirm / toast)
// Ensure ui utilities are loaded
(function(){
  const s = document.createElement('script');
  s.src = '/assets/js/utils/ui.js';
  document.head.appendChild(s);
})();

// Simple helper to fetch json
async function fetchJSON(url, opts){
  const res = await fetch(url, opts);
  return res.json();
}

window.fetchJSON = fetchJSON; // expose for controllers
