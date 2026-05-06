const menuBtn = document.querySelector(".menu-btn");
const nav = document.querySelector(".nav");

if (menuBtn && nav) {
  menuBtn.addEventListener("click", () => {
    nav.classList.toggle("active");
  });
}

const loader = document.querySelector(".loader");

window.addEventListener("load", () => {
  if (loader) {
    loader.classList.add("hidden");
  }

  const galleryImages = document.querySelectorAll(".gallery img");

  galleryImages.forEach((img, index) => {
    setTimeout(() => {
      img.classList.add("visible");
    }, index * 100);
  });
});

const lightbox = document.querySelector(".lightbox");
const lightboxImg = document.querySelector(".lightbox img");
const closeLightbox = document.querySelector(".close-lightbox");

document.querySelectorAll(".gallery img").forEach(img => {
  img.addEventListener("click", () => {
    if (!lightbox || !lightboxImg) return;

    lightboxImg.src = img.src;
    lightbox.classList.add("active");
  });
});

if (closeLightbox && lightbox) {
  closeLightbox.addEventListener("click", () => {
    lightbox.classList.remove("active");
  });

  lightbox.addEventListener("click", e => {
    if (e.target === lightbox) {
      lightbox.classList.remove("active");
    }
  });
}

document.addEventListener("keydown", e => {
  if (e.key === "Escape" && lightbox) {
    lightbox.classList.remove("active");
  }
});