@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap');

:root{
  --black:#050505;--soft:#0d0d0d;--white:#f7f2ea;--muted:#b9b1a7;
  --gold:#c6a15b;--line:rgba(255,255,255,.13);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--black);color:var(--white);font-family:Inter,sans-serif}
a{text-decoration:none;color:inherit}
img{width:100%;display:block;object-fit:cover}
.nav{position:fixed;top:0;width:100%;z-index:1000;padding:24px 7%;display:flex;justify-content:space-between;align-items:center;background:rgba(5,5,5,.68);backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}
.logo{font-family:'Playfair Display',serif;font-size:22px}
.links{display:flex;gap:32px;font-size:12px;text-transform:uppercase;letter-spacing:2px}
.links a{color:var(--muted)}.links a:hover,.links .active{color:var(--white)}
.hero{padding:160px 7% 90px}
.hero.full{min-height:100vh;display:grid;grid-template-columns:1.1fr .9fr;gap:60px;align-items:center;background:linear-gradient(to right,rgba(5,5,5,.92),rgba(5,5,5,.45)),url('images/hero.jpg');background-size:cover;background-position:center}
.eyebrow{color:var(--gold);text-transform:uppercase;letter-spacing:4px;font-size:12px;margin-bottom:22px}
h1{font-family:'Playfair Display',serif;font-size:clamp(54px,8vw,112px);line-height:.92;margin-bottom:24px}
h2{font-family:'Playfair Display',serif;font-size:clamp(44px,6vw,82px);line-height:1;margin-bottom:24px}
h3{font-family:'Playfair Display',serif}
p{color:var(--muted);line-height:1.8}
.btns{display:flex;gap:16px;flex-wrap:wrap;margin-top:32px}
.btn{padding:15px 26px;border:1px solid var(--white);text-transform:uppercase;letter-spacing:2px;font-size:12px;transition:.3s}
.btn.primary{background:var(--white);color:var(--black)}
.btn:hover{background:var(--gold);border-color:var(--gold);color:var(--black)}
section{padding:100px 7%}
.split{display:grid;grid-template-columns:.9fr 1.1fr;gap:55px;align-items:center}
.split img,.hero-card img{height:560px}
.hero-card{border:1px solid var(--line);padding:24px;background:rgba(0,0,0,.45)}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.item{position:relative;height:430px;overflow:hidden;background:var(--soft)}
.item.tall{height:560px}
.item img{height:100%;transition:.7s ease;filter:contrast(1.05)}
.item:hover img{transform:scale(1.08);opacity:.72}
.label{position:absolute;bottom:22px;left:22px;right:22px}
.label h3{font-size:28px}.label span{color:var(--gold);font-size:11px;text-transform:uppercase;letter-spacing:2px}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.card{border:1px solid var(--line);padding:32px;background:var(--soft);transition:.3s}
.card:hover{border-color:var(--gold);transform:translateY(-6px)}
.card h3{font-size:30px;margin-bottom:14px}
.price{margin-top:24px;color:var(--gold);font-size:12px;text-transform:uppercase;letter-spacing:2px}
form{display:grid;gap:16px}
input,select,textarea{width:100%;background:transparent;border:1px solid var(--line);padding:16px;color:var(--white);font-family:inherit}
textarea{min-height:150px}
button{background:var(--white);color:var(--black);border:none;padding:16px;text-transform:uppercase;letter-spacing:2px;font-weight:800;cursor:pointer}
button:hover{background:var(--gold)}
.socials a{display:inline-block;margin:10px 12px;border:1px solid var(--line);padding:12px 18px;text-transform:uppercase;font-size:11px;letter-spacing:2px}
.socials a:hover{background:var(--gold);color:var(--black)}
footer{padding:34px 7%;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:1.5px}
.reveal{opacity:0;transform:translateY(24px);transition:1s ease}
.reveal.show{opacity:1;transform:translateY(0)}
@media(max-width:1000px){.hero.full,.split{grid-template-columns:1fr}.grid,.cards{grid-template-columns:repeat(2,1fr)}}
@media(max-width:650px){.links{gap:12px;font-size:9px}.grid,.cards{grid-template-columns:1fr}.item,.item.tall,.split img,.hero-card img{height:420px}}
