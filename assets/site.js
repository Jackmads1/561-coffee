// shared by every page: bag count, add to bag buttons, current page in the nav, and the cream sheet page change
(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches,D=document;
  function get(){try{return +localStorage.getItem('bag561')||0}catch(e){return 0}}
  function set(n){try{localStorage.setItem('bag561',n)}catch(e){}}
  var bagLink=D.querySelector('nav .r a');
  function show(){if(bagLink)bagLink.textContent='bag ('+get()+')'}
  show();
  D.querySelectorAll('.prod .add').forEach(function(b){
    b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();set(get()+1);show();
      b.textContent='Added';b.classList.add('ok');clearTimeout(b._t);b._t=setTimeout(function(){b.textContent='Add to bag';b.classList.remove('ok')},1300)});
  });

  // mark the page you are on
  var here=(location.pathname.split('/').pop()||'index.html');
  D.querySelectorAll('nav .l a').forEach(function(a){if(a.getAttribute('href')===here)a.style.opacity='.55'});

  // page change
  var veil=D.getElementById('veil');if(veil)veil.style.animation='none';
  if(!veil){veil=D.createElement('div');veil.id='veil';veil.setAttribute('aria-hidden','true');veil.className='gone';veil.style.transition='none';veil.style.animation='none';D.body.appendChild(veil)}
  else{requestAnimationFrame(function(){requestAnimationFrame(function(){veil.classList.add('gone')})})}
  D.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a');if(!a||reduce||e.metaKey||e.ctrlKey||e.shiftKey||a.target)return;
    var href=a.getAttribute('href')||'';if(!/\.html(#.*)?$/.test(href))return;
    var file=href.split('#')[0];if(file===here&&href.indexOf('#')>-1)return;
    e.preventDefault();
    veil.style.transition='none';veil.className='below';void veil.offsetWidth;veil.style.transition='';veil.className='cover';
    setTimeout(function(){location.href=href},680);
  });
  addEventListener('pageshow',function(e){if(e.persisted){veil.style.transition='none';veil.className='gone'}});
})();
