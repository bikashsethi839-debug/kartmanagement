// Minimal UI utilities: modal and toast
window.UI = (function(){
  function createModal(){
    if(document.getElementById('app-modal')) return;
    const div = document.createElement('div');
    div.id = 'app-modal';
    div.innerHTML = `
      <div class="modal-backdrop" id="modal-backdrop">
        <div class="modal-card" role="dialog" aria-modal="true">
          <div class="modal-body" id="modal-body"></div>
          <div class="modal-actions" id="modal-actions"></div>
        </div>
      </div>`;
    document.body.appendChild(div);
    div.addEventListener('click', (e)=>{ if(e.target.id==='modal-backdrop') hide(); });
  }

  function show(options){
    createModal();
    const body = document.getElementById('modal-body');
    const actions = document.getElementById('modal-actions');
    body.innerHTML = options.html || '';
    actions.innerHTML = '';
    (options.buttons||[]).forEach(b=>{
      const btn = document.createElement('button');
      btn.textContent = b.text;
      btn.className = b.className || '';
      btn.addEventListener('click', ()=>{ if(b.onClick) b.onClick(); if(b.close !== false) hide(); });
      actions.appendChild(btn);
    });
    document.getElementById('app-modal').style.display = 'block';
    return document.getElementById('app-modal');
  }

  function hide(){
    const m = document.getElementById('app-modal');
    if(m) m.style.display = 'none';
  }

  function confirm(message){
    return new Promise(resolve=>{
      show({html:`<p>${message}</p>`, buttons:[{text:'Cancel', className:'btn-cancel', onClick:()=>resolve(false)},{text:'OK', className:'btn-ok', onClick:()=>resolve(true)}]});
    });
  }

  function toast(message, timeout=3000){
    let container = document.getElementById('toast-container');
    if(!container){ container = document.createElement('div'); container.id = 'toast-container'; document.body.appendChild(container);} 
    const el = document.createElement('div'); el.className = 'toast'; el.textContent = message; container.appendChild(el);
    setTimeout(()=>{ el.classList.add('visible'); }, 10);
    setTimeout(()=>{ el.classList.remove('visible'); setTimeout(()=>el.remove(),300); }, timeout);
  }

  return { show, hide, confirm, toast };
})();
