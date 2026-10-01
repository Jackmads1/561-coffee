# Builds shop.html, about.html and spots.html from index.html, so every page shares the same styles, nav, closing block and footer.
# Run from the repo root: python3 _build/pages.py
import re, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
idx = (R / 'index.html').read_text()

head_css = re.search(r'<style>\n(.*?)</style>', idx, re.S).group(1)
nav = re.search(r'<nav id="nav">.*?</nav>', idx, re.S).group(0)
close = re.search(r'<section class="close io".*?</section>', idx, re.S).group(0)
foot = re.search(r'<footer.*?</footer>', idx, re.S).group(0)
fonts = re.search(r'<link rel="preconnect".*?rel="stylesheet">', idx, re.S).group(0)

# links on sub pages point back into the home page
def home(s):
    return re.sub(r'href="#(top|spots|menu)"', lambda m: 'href="index.html' + ('' if m.group(1) == 'top' else '#' + m.group(1)) + '"', s)
nav_s, close_s, foot_s = home(nav), home(close), home(foot)

PAGE_CSS = r'''
/* ---- sub pages ---- */
.page{padding-top:clamp(60px,5.6vw,84px)}
.phead{padding:clamp(70px,13vh,150px) clamp(14px,2.5vw,36px) clamp(34px,6vh,60px);text-align:center}
.phead .huge{font-size:clamp(64px,12vw,200px)}
.phead .sub{color:#6f5c4a}
.chips{display:flex;justify-content:center;gap:8px;margin-top:30px;flex-wrap:wrap}
.chips button{padding:9px 16px;border:1px solid #cdbba5;font:700 9.5px Archivo,sans-serif;letter-spacing:.12em;text-transform:uppercase;transition:background .25s,color .25s,border-color .25s}
.chips button.on,.chips button:hover{background:var(--ink);color:var(--cream);border-color:var(--ink)}
.chips sup{font-size:8px;margin-left:4px;opacity:.6}
.sgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(14px,1.6vw,26px);padding:0 clamp(14px,2.5vw,36px) clamp(70px,11vh,130px);text-align:left}
.sgrid .prod{transition:opacity .5s,transform .5s cubic-bezier(.2,.75,.15,1)}
.sgrid .prod.off{display:none}
.prod .add{position:absolute;left:12px;right:12px;bottom:12px;padding:12px;background:var(--paper);color:var(--ink);font:800 9.5px Archivo,sans-serif;letter-spacing:.12em;text-transform:uppercase;opacity:0;transform:translateY(8px);transition:opacity .35s,transform .45s cubic-bezier(.2,.75,.15,1),background .25s,color .25s;z-index:2}
.prod:hover .add,.prod .add:focus{opacity:1;transform:none}
.prod .add:hover{background:var(--ink);color:var(--cream)}
.prod .add.ok{background:var(--ink);color:var(--cream)}
@media (hover:none){.prod .add{opacity:1;transform:none;left:auto;right:8px;bottom:8px;padding:9px 11px}}
.facts{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid #ddcfbc;border-bottom:1px solid #ddcfbc;margin:0 clamp(14px,2.5vw,36px)}
.facts div{padding:26px 20px;text-align:center;border-right:1px solid #ddcfbc}.facts div:last-child{border-right:0}
.facts b{display:block;font:900 clamp(20px,2vw,28px)/1 Archivo,sans-serif;letter-spacing:-.02em;text-transform:uppercase}
.facts span{display:block;margin-top:8px;font:italic 400 clamp(15px,1.3vw,19px) 'Instrument Serif',Georgia,serif;color:#6f5c4a}
.pad{height:clamp(60px,10vh,120px)}

/* about */
.ahero{position:relative;height:100vh;height:100svh;overflow:hidden;background:var(--black)}
.ahero img{position:absolute;inset:-6% 0;width:100%;height:112%;object-fit:cover;object-position:56% 50%;will-change:transform}
.ahero::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(43,30,22,.1),rgba(43,30,22,.35))}
.ahero .tx{position:absolute;left:0;right:0;bottom:12vh;text-align:center;z-index:2;text-shadow:0 1px 26px rgba(43,30,22,.45)}
.ahero .huge{font-size:clamp(64px,12vw,200px)}
.ahero .kicker{color:var(--cream)}
.lede{max-width:880px;margin:0 auto;font:400 clamp(28px,3.4vw,52px)/1.08 'Instrument Serif',Georgia,serif;letter-spacing:-.01em}
.lede em{color:#d2b48c}
.split{display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:clamp(24px,5vw,90px);padding:clamp(50px,9vh,110px) clamp(14px,6vw,110px);background:var(--black)}
.split.flip figure{order:2}
.split figure{margin:0;aspect-ratio:.8;overflow:hidden}
.split figure img,.split figure video{width:100%;height:100%;object-fit:cover;transform:scale(1.12);will-change:transform}
.split .n{font:italic 400 clamp(17px,1.5vw,22px) 'Instrument Serif',Georgia,serif;color:#d2b48c}
.split h2{font:900 clamp(38px,5vw,84px)/.9 Archivo,sans-serif;letter-spacing:-.035em;text-transform:uppercase;margin:10px 0 18px}
.split p{max-width:42ch;margin:0;font-size:14px;line-height:1.6;color:#e9dccb}
.nums{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:0 clamp(14px,2.5vw,36px)}
.nums div{padding:clamp(28px,5vh,50px) 16px;text-align:center;border-right:1px solid var(--line)}.nums div:last-child{border-right:0}
.nums b{display:block;font:900 clamp(56px,8vw,130px)/.85 Archivo,sans-serif;letter-spacing:-.04em}
.nums span{display:block;margin-top:12px;font:800 9.5px Archivo,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#c4ae95}
.draft{margin:14px 0 0;font:600 9.5px Archivo,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#a08a74}

@media (max-width:760px){
 .sgrid{grid-template-columns:1fr 1fr;gap:12px 10px}
 .prod h3{font-size:10.5px}.prod p{font-size:9.5px}
 .facts,.nums{grid-template-columns:1fr}.facts div,.nums div{border-right:0;border-bottom:1px solid #ddcfbc}.nums div{border-bottom-color:var(--line)}.facts div:last-child,.nums div:last-child{border-bottom:0}
 .split,.split.flip{grid-template-columns:1fr;padding:50px 16px}.split.flip figure{order:0}
}
@media (min-width:761px) and (max-width:1100px){.sgrid{grid-template-columns:repeat(3,1fr)}}
'''

# shared script for sub pages: smooth scroll, nav hide on scroll, reveals, parallax, bag count, page change
PAGE_JS = r'''<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script>
(function(){
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var lenis=null;try{if(!reduce&&window.Lenis)lenis=new Lenis({lerp:.09,smoothWheel:true})}catch(e){lenis=null}
function clamp(v,a,b){return v<a?a:v>b?b:v}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.2});
document.querySelectorAll('.io,.rv').forEach(function(el){io.observe(el)});
var nav=document.getElementById('nav'),ny=0,pxs=[].slice.call(document.querySelectorAll('.px')),H=innerHeight;addEventListener('resize',function(){H=innerHeight});
function frame(t){if(lenis)lenis.raf(t);var y=scrollY,dy=y-ny;if(Math.abs(dy)>6){nav.classList.toggle('up',dy>0&&y>120);ny=y}if(y<=120)nav.classList.remove('up');
  if(!reduce)pxs.forEach(function(im){var r=im.parentNode.getBoundingClientRect();if(r.bottom<0||r.top>H)return;var q=clamp((H-r.top)/(H+r.height),0,1);im.style.transform=(im.dataset.s?'scale(1.12) ':'')+'translateY('+((q-.5)*(im.dataset.s?-8:-10))+'%)'});
  requestAnimationFrame(frame)}
requestAnimationFrame(frame);
@@PAGE@@
})();
</script>
<script src="assets/site.js"></script>'''

SHOP_JS = r'''// filter chips
var chips=[].slice.call(document.querySelectorAll('.chips button')),cards=[].slice.call(document.querySelectorAll('.sgrid .prod'));
chips.forEach(function(c){c.addEventListener('click',function(){chips.forEach(function(o){o.classList.toggle('on',o===c)});var f=c.dataset.f;
  cards.forEach(function(p,i){var show=f==='all'||p.dataset.cat===f;p.classList.toggle('off',!show);if(show){p.classList.remove('in');void p.offsetWidth;setTimeout(function(){p.classList.add('in')},40+i%4*60)}});
  if(lenis)lenis.resize()})});'''

def page(title, desc, body, js='', head='', closing=True):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{fonts}
<style>
{head_css}{PAGE_CSS}</style>
{head}
</head>
<body class="page">
<div id="veil" aria-hidden="true"></div>
{nav_s}
{body}
{close_s if closing else ''}

{foot_s}
{PAGE_JS.replace('@@PAGE@@', js)}
</body>
</html>
'''

def prod(cat, img, alt, name, notes, price, hover=None):
    h = f'<img class="alt" src="assets/{hover}.jpg" alt="" loading="lazy">' if hover else ''
    return f'''    <article class="prod rv" data-cat="{cat}" data-name="{name}"><div class="ph"><img src="assets/{img}.jpg" alt="{alt}" loading="lazy">{h}<button class="add" type="button">Add to bag</button></div><div class="meta"><div><h3>{name}</h3><p>{notes}</p></div><div class="pr">{price}</div></div></article>'''

# the products are read from the home page's shop row, so both stay the same
items = []
for m in re.finditer(r'<article class="prod rv"><div class="ph"><img src="assets/([\w-]+)\.jpg" alt="([^"]+)" loading="lazy">(?:<img class="alt" src="assets/([\w-]+)\.jpg"[^>]*>)?</div><div class="meta"><div><h3>([^<]+)</h3><p>([^<]+)</p></div><div class="pr">(.*?)</div></div></article>', idx):
    img, alt, hov, name, notes, price = m.groups()
    items.append(prod('merch' if img.startswith('m-') else 'coffee', img, alt, name, notes, price, hov))
nc = sum(1 for i in items if 'data-cat="coffee"' in i); nm = len(items) - nc

shop_body = f'''<main>
<section class="white phead io">
  <p class="kicker serif">Roasted weekly in San Antonio</p>
  <h1 class="huge"><span class="ln"><span>Shop</span></span></h1>
  <p class="sub">Five small-batch coffees in 12 oz whole bean bags, plus a few things to drink them from.</p>
  <div class="chips rv"><button class="on" data-f="all">All<sup>{len(items)}</sup></button><button data-f="coffee">Coffee<sup>{nc}</sup></button><button data-f="merch">Merch<sup>{nm}</sup></button></div>
</section>
<section class="white">
  <div class="sgrid">
{chr(10).join(items)}
  </div>
  <div class="facts rv"><div><b>Small batch</b><span>Roasted a little at a time</span></div><div><b>Roasted weekly</b><span>Fresh out of San Antonio</span></div><div><b>Whole bean</b><span>12 oz bags, grind at home</span></div></div>
  <div class="pad"></div>
</section>
</main>'''

about_body = '''<main>
<section class="ahero io" data-nav="dark">
  <img class="px" src="assets/hero-arch.jpg" alt="An espresso machine on a stone counter under a sunlit plaster arch">
  <div class="tx"><p class="kicker serif rv">Our story</p><h1 class="huge"><span class="ln"><span>About</span></span><span class="ln"><span>561</span></span></h1></div>
</section>

<section class="stmt io">
  <p class="lede rv">561 is a small coffee roaster in San Antonio. We roast <em>a little at a time, every week,</em> and pour it straight. No fuss, no attitude, just coffee we would drink ourselves.</p>
  <p class="draft">Draft copy</p>
</section>

<section class="split io">
  <figure><video class="px" data-s="1" src="assets/beans.mp4" poster="assets/beans.jpg" autoplay muted loop playsinline preload="metadata" aria-label="Freshly roasted beans with smoke rising"></video></figure>
  <div class="rv"><span class="n">01</span><h2>Roasted<br>weekly</h2><p>Every bag is roasted in a small batch and sent out while it is still fresh. If it has been sitting on a shelf for months, it is not ours.</p></div>
</section>
<section class="split flip io">
  <figure><img class="px" data-s="1" src="assets/pair-tamper.jpg" alt="A walnut espresso tamper on a sunlit stone counter" loading="lazy"></figure>
  <div class="rv"><span class="n">02</span><h2>Five<br>coffees</h2><p>Signature, Ocean, Colombian, Espresso and Decaf. A short list on purpose, so each one gets the attention it deserves.</p></div>
</section>
<section class="split io">
  <figure><video class="px" data-s="1" src="assets/pour.mp4" poster="assets/pour.jpg" autoplay muted loop playsinline preload="metadata" aria-label="Latte art being poured"></video></figure>
  <div class="rv"><span class="n">03</span><h2>Made to<br>share</h2><p>Coffee is better with people around it. Before class, after practice, or on a slow Sunday, pour one and pass it on.</p></div>
</section>

<section class="stmt io" style="padding-bottom:0">
  <div class="nums rv"><div><b>5</b><span>Coffees</span></div><div><b>12</b><span>Ounce bags</span></div><div><b>1</b><span>Roaster in San Antonio</span></div></div>
</section>

<section class="stmt io">
  <h2 class="huge"><span class="ln"><span>Taste it</span></span><span class="ln"><span>for yourself</span></span></h2>
  <a class="btn" href="shop.html">Shop coffee</a>
</section>
</main>'''


# ---- spots page: list on the left, map on the right ----
import json
SPOTS = [
    # name, address line, city, lat, lng, note
    ('Thomas Hall', 'Trinity University, One Trinity Place', 'San Antonio, TX 78212', 29.4624, -98.4832, 'On campus at Trinity University'),
]

SPOTS_CSS = r"""<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
.spage{display:grid;grid-template-columns:minmax(320px,28%) 1fr;height:calc(100vh - clamp(60px,5.6vw,84px));height:calc(100svh - clamp(60px,5.6vw,84px));background:var(--paper);color:var(--ink)}
.slist{overflow:auto;padding:clamp(26px,4vh,44px) clamp(18px,2vw,32px);border-right:1px solid #ddcfbc}
.slist h1{font:400 clamp(24px,2vw,32px)/1.1 'Instrument Serif',Georgia,serif;color:#8a7662;margin:0 0 18px}
.sfind{display:flex;gap:8px;margin-bottom:clamp(26px,5vh,48px)}
.sfind input{flex:1;min-width:0;height:52px;padding:0 16px;border:1px solid #c9b18f;background:transparent;font:500 13px Archivo,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);outline:none;border-radius:0}
.sfind input:focus{border-color:var(--ink)}
.sfind button{width:58px;height:52px;background:#b59a72;color:var(--paper);display:grid;place-items:center;transition:background .25s}
.sfind button:hover{background:var(--ink)}
.sfind svg{width:24px;height:24px}
.spot{padding:20px 14px 22px;border-bottom:1px solid #ddcfbc;cursor:pointer;transition:background .25s}
.spot:hover,.spot.on{background:#ebe1d2}
.spot h2{font:800 clamp(19px,1.5vw,24px)/1.15 Archivo,sans-serif;letter-spacing:-.01em;margin:0 0 10px}
.spot .ad{display:flex;gap:10px;align-items:flex-start;font:400 13.5px/1.45 Archivo,sans-serif;color:#4c3d31}
.spot .ad svg{flex:none;width:14px;height:19px;margin-top:1px;fill:#b59a72}
.spot .ln{margin-top:12px;font:500 12.5px Archivo,sans-serif;color:var(--ink)}
.spot .ln a{text-decoration:underline;text-underline-offset:3px}
.spot .ln span{margin:0 6px;color:#9c8873}
.snone{display:none;font:400 14px/1.5 Archivo,sans-serif;color:#6f5c4a;padding:14px}
.smap{position:relative;background:#e9e2d6}
.smap #map{position:absolute;inset:0}
.pin561{width:46px;height:46px;border-radius:50%;background:var(--black);color:var(--cream);display:grid;place-items:center;font:400 17px/1 'Instrument Serif',Georgia,serif;letter-spacing:.02em;box-shadow:0 0 0 3px var(--paper),0 6px 16px rgba(0,0,0,.35);transition:transform .3s cubic-bezier(.2,.75,.15,1)}
.pin561.on{transform:scale(1.18)}
.leaflet-container{font-family:Archivo,sans-serif}
.leaflet-popup-content-wrapper{border-radius:0;background:var(--paper);color:var(--ink)}
.leaflet-popup-content{margin:14px 16px;font:400 13px/1.4 Archivo,sans-serif}
.leaflet-popup-content b{display:block;font-weight:800;font-size:14px;margin-bottom:4px}
.leaflet-popup-tip{background:var(--paper)}
.leaflet-bar a{border-radius:0!important;color:var(--ink)}
.me{width:16px;height:16px;border-radius:50%;background:#3b82f6;box-shadow:0 0 0 4px rgba(59,130,246,.25),0 0 0 1.5px #fff inset}
@media (max-width:860px){.spage{grid-template-columns:1fr;grid-template-rows:auto auto;height:auto}.slist{border-right:0;overflow:visible}.smap{order:-1;height:62vh}}
</style>"""

PIN = '<svg viewBox="0 0 14 19" aria-hidden="true"><path d="M7 0a7 7 0 0 0-7 7c0 5 7 12 7 12s7-7 7-12a7 7 0 0 0-7-7zm0 9.6A2.6 2.6 0 1 1 7 4.4a2.6 2.6 0 0 1 0 5.2z"/></svg>'

def spot(i, sp):
    name, line, city, lat, lng, note = sp
    q = (name + ' ' + line + ' ' + city).lower()
    return ('    <article class="spot" data-i="%d" data-q="%s"><h2>561 Coffee - %s</h2><div class="ad">%s<span>%s, %s</span></div>'
            '<div class="ln"><a href="https://www.google.com/maps/dir/?api=1&amp;destination=%s,%s" target="_blank" rel="noopener">Get directions</a><span>-</span><a href="#" class="go">Show on map</a></div></article>'
            % (i, q, name, PIN, line, city, lat, lng))

spots_body = '''<main class="spage" data-nav="light">
  <aside class="slist">
    <h1>Find your 561 Coffee spot</h1>
    <form class="sfind" role="search" onsubmit="return false"><input id="sq" type="search" placeholder="Search a city" aria-label="Search a city" autocomplete="off"><button type="button" id="sme" aria-label="Use my location"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="6.5"/><circle cx="12" cy="12" r="2.2" fill="currentColor"/><path d="M12 1.5v3.5M12 19v3.5M1.5 12H5M19 12h3.5"/></svg></button></form>
''' + '\n'.join(spot(i, sp) for i, sp in enumerate(SPOTS)) + '''
    <p class="snone" id="snone">No spots there yet. We are only in San Antonio for now.</p>
  </aside>
  <div class="smap" data-lenis-prevent><div id="map" role="region" aria-label="Map of 561 Coffee spots"></div></div>
</main>'''

SPOTS_JS = r"""// map
var SP=@@SPOTS@@;
if(window.L){
  var map=L.map('map',{zoomControl:false}).setView([SP[0][3],SP[0][4]],16);
  L.control.zoom({position:'topright'}).addTo(map);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
  var cards=[].slice.call(document.querySelectorAll('.spot')),marks=SP.map(function(s,i){
    var m=L.marker([s[3],s[4]],{icon:L.divIcon({className:'',html:'<div class="pin561">561</div>',iconSize:[46,46],iconAnchor:[23,23],popupAnchor:[0,-26]}),title:s[0]}).addTo(map)
      .bindPopup('<b>561 Coffee - '+s[0]+'</b>'+s[1]+'<br>'+s[2]+'<br><span style="color:#8a7662">'+s[5]+'</span>');
    m.on('click',function(){pick(i,false)});return m});
  function pick(i,fly){cards.forEach(function(c,j){c.classList.toggle('on',j===i)});marks.forEach(function(m,j){var e=m.getElement();if(e)e.firstChild.classList.toggle('on',j===i)});
    if(fly){map.flyTo([SP[i][3],SP[i][4]],17,{duration:.9});setTimeout(function(){marks[i].openPopup()},700)}}
  cards.forEach(function(c,i){c.addEventListener('click',function(e){var a=e.target.closest('a');if(a&&!a.classList.contains('go'))return;e.preventDefault();pick(i,true)})});
  if(SP.length>1)map.fitBounds(L.latLngBounds(SP.map(function(s){return [s[3],s[4]]})).pad(.3));
  // search a city
  var q=document.getElementById('sq'),none=document.getElementById('snone');
  q.addEventListener('input',function(){var v=q.value.trim().toLowerCase(),n=0;cards.forEach(function(c){var ok=!v||c.dataset.q.indexOf(v)>-1;c.style.display=ok?'':'none';if(ok)n++});none.style.display=n?'none':'block'});
  // use my location
  var me=null;document.getElementById('sme').addEventListener('click',function(){if(!navigator.geolocation)return;
    navigator.geolocation.getCurrentPosition(function(p){var ll=[p.coords.latitude,p.coords.longitude];
      if(me)me.setLatLng(ll);else me=L.marker(ll,{icon:L.divIcon({className:'',html:'<div class="me"></div>',iconSize:[16,16],iconAnchor:[8,8]}),title:'You'}).addTo(map);
      var near=0,best=1e9;SP.forEach(function(s,i){var d=Math.pow(s[3]-ll[0],2)+Math.pow(s[4]-ll[1],2);if(d<best){best=d;near=i}});
      map.flyToBounds(L.latLngBounds([ll,[SP[near][3],SP[near][4]]]).pad(.35),{duration:1});pick(near,false)},function(){},{timeout:9000})});
}"""

(R / 'shop.html').write_text(page('Shop | 561 Coffee', 'Shop 561 Coffee: five small-batch coffees roasted weekly in San Antonio, plus mugs, tumblers and bottles.', shop_body, SHOP_JS))
(R / 'about.html').write_text(page('About | 561 Coffee', 'The story behind 561 Coffee, a small-batch roaster in San Antonio.', about_body))
(R / 'spots.html').write_text(page('Spots | 561 Coffee', 'Find 561 Coffee: where to grab a cup in San Antonio.', spots_body, SPOTS_JS.replace('@@SPOTS@@', json.dumps(SPOTS)), SPOTS_CSS, closing=False))
print('built shop.html (%d products), about.html and spots.html' % len(items))
