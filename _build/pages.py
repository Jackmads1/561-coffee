# Builds shop.html and about.html from index.html, so every page shares the same styles, nav, closing block and footer.
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

def page(title, desc, body, js=''):
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
</head>
<body class="page">
<div id="veil" aria-hidden="true"></div>
{nav_s}
{body}
{close_s}

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

(R / 'shop.html').write_text(page('Shop | 561 Coffee', 'Shop 561 Coffee: five small-batch coffees roasted weekly in San Antonio, plus mugs, tumblers and bottles.', shop_body, SHOP_JS))
(R / 'about.html').write_text(page('About | 561 Coffee', 'The story behind 561 Coffee, a small-batch roaster in San Antonio.', about_body))
print('built shop.html (%d products) and about.html' % len(items))
