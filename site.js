(function(){
  var KEY='kj-cookie-consent';
  function get(){try{return localStorage.getItem(KEY);}catch(e){return null;}}
  function set(v){try{localStorage.setItem(KEY,v);}catch(e){}}
  var box=document.createElement('div');
  box.className='kj-cookie';box.hidden=true;
  box.setAttribute('role','dialog');box.setAttribute('aria-label','Süti beállítások');
  box.innerHTML='<b>Sütik és adatvédelem</b>'+
    '<p>Az oldal működéséhez szükséges technikai tárolást használunk (pl. ez a döntésed). Marketing vagy statisztikai sütit jelenleg nem alkalmazunk; ha később bevezetünk, csak a hozzájárulásoddal. Részletek: <a href="sutik.html">Süti tájékoztató</a>, <a href="adatvedelem.html">Adatkezelési tájékoztató</a>.</p>'+
    '<div class="row"><button type="button" class="btn btn-red" data-c="all">Elfogadom</button>'+
    '<button type="button" class="btn btn-outline" data-c="necessary">Csak a szükségesek</button></div>';
  box.addEventListener('click',function(e){
    var c=e.target.getAttribute&&e.target.getAttribute('data-c');
    if(!c)return;set(c);box.hidden=true;
    document.dispatchEvent(new CustomEvent('kj-consent',{detail:c}));
  });
  function init(){
    document.body.appendChild(box);
    if(!get())box.hidden=false;
    document.querySelectorAll('[data-cookie-settings]').forEach(function(b){
      b.addEventListener('click',function(){box.hidden=false;});
    });
  }
  window.kjConsent=get;
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
