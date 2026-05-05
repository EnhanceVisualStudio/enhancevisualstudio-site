const loader = document.querySelector(".loader");

window.addEventListener("load", () => {
  if (loader) loader.classList.add("hidden");

  const galleryImages = document.querySelectorAll(".gallery img");
  galleryImages.forEach((img, index) => {
    setTimeout(() => {
      img.classList.add("visible");
    }, index * 100);
  });
});

const menuBtn = document.querySelector(".menu-btn");
const nav = document.querySelector(".nav");

if (menuBtn && nav) {
  menuBtn.addEventListener("click", () => {
    nav.classList.toggle("active");
  });
}

const slides = document.querySelectorAll(".slide");
const currentSlide = document.getElementById("currentSlide");
let slideIndex = 0;

function showSlide() {
  if (!slides.length) return;

  slides.forEach(slide => slide.classList.remove("active"));
  slides[slideIndex].classList.add("active");

  if (currentSlide) {
    currentSlide.textContent = String(slideIndex + 1).padStart(2, "0");
  }

  slideIndex = (slideIndex + 1) % slides.length;
}

if (slides.length) {
  showSlide();
  setInterval(showSlide, 4500);
}

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
