const menuBtn = document.querySelector(".menu-btn");
const nav = document.querySelector(".nav");

if (menuBtn && nav) {
  menuBtn.addEventListener("click", () => {
    nav.classList.toggle("active");
  });
}

/* LIGHTBOX */
const lightbox = document.querySelector(".lightbox");
const lightboxImg = document.querySelector(".lightbox img");
const closeLightbox = document.querySelector(".close-lightbox");

document.querySelectorAll(".gallery img").forEach(img => {
  img.addEventListener("click", () => {
    lightboxImg.src = img.src;
    lightbox.classList.add("active");
  });
});

closeLightbox.addEventListener("click", () => {
  lightbox.classList.remove("active");
});

lightbox.addEventListener("click", e => {
  if (e.target === lightbox) {
    lightbox.classList.remove("active");
  }
});

document.addEventListener("keydown", e => {
  if (e.key === "Escape") {
    lightbox.classList.remove("active");
  }
});