/* PRELOADER */
window.addEventListener("load", ()=>{
    const loader = document.getElementById("loader");
    setTimeout(()=>{
        loader.style.opacity = "0";
        loader.style.pointerEvents = "none";
    }, 1200);
});

/* NAV SCROLL */
window.addEventListener("scroll", ()=>{
    document.querySelector("nav").classList.toggle("scrolled", window.scrollY > 50);
});

/* PAGE TRANSITION */
const transition = document.createElement("div");
transition.classList.add("transition");
document.body.appendChild(transition);

document.querySelectorAll("a").forEach(link=>{
    link.addEventListener("click", function(e){
        if(this.href.includes(window.location.origin)){
            e.preventDefault();
            transition.classList.add("active");
            setTimeout(()=> window.location = this.href, 800);
        }
    });
});

/* REVEAL */
function reveal(){
    document.querySelectorAll(".reveal").forEach(el=>{
        let top = el.getBoundingClientRect().top;
        if(top < window.innerHeight - 100){
            el.classList.add("active");
        }
    });
}
window.addEventListener("scroll", reveal);

/* CUSTOM CURSOR */
const cursor = document.createElement("div");
cursor.classList.add("cursor");
document.body.appendChild(cursor);

document.addEventListener("mousemove", e=>{
    cursor.style.left = e.clientX + "px";
    cursor.style.top = e.clientY + "px";
});

/* CURSOR INTERACTION */
document.querySelectorAll("a, button").forEach(el=>{
    el.addEventListener("mouseenter", ()=> cursor.classList.add("active"));
    el.addEventListener("mouseleave", ()=> cursor.classList.remove("active"));
});

/* MAGNETIC EFFECT */
document.querySelectorAll(".magnetic").forEach(btn=>{
    btn.addEventListener("mousemove", e=>{
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width/2;
        const y = e.clientY - rect.top - rect.height/2;
        btn.style.transform = `translate(${x*0.2}px, ${y*0.2}px)`;
    });

    btn.addEventListener("mouseleave", ()=>{
        btn.style.transform = "translate(0,0)";
    });
});

/* PARALLAX */
document.querySelectorAll(".parallax").forEach(section=>{
    section.addEventListener("mousemove", e=>{
        const img = section.querySelector("img");
        const x = (window.innerWidth/2 - e.clientX) / 40;
        const y = (window.innerHeight/2 - e.clientY) / 40;
        img.style.transform = `translate(${x}px, ${y}px) scale(1.05)`;
    });
});