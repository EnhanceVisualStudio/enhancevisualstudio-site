/* NAV SCROLL */
window.addEventListener("scroll", ()=>{
    document.querySelector("nav").classList.toggle("scrolled", window.scrollY > 50);
});

/* PAGE TRANSITION */
document.querySelectorAll("a").forEach(link=>{
    link.addEventListener("click", function(e){
        if(this.href && this.href.includes(window.location.origin)){
            e.preventDefault();
            document.body.classList.add("fade-out");
            setTimeout(()=> window.location = this.href, 400);
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

/* CURSOR */
const cursor = document.createElement("div");
cursor.classList.add("cursor");
document.body.appendChild(cursor);

document.addEventListener("mousemove", e=>{
    cursor.style.left = e.clientX + "px";
    cursor.style.top = e.clientY + "px";
});