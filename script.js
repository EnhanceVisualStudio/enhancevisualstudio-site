const menuBtn = document.querySelector(".menu-btn");
const nav = document.querySelector(".nav");

if (menuBtn && nav) {
  menuBtn.addEventListener("click", () => {
    nav.classList.toggle("active");
  });
}

/* PORTFOLIO LIGHTBOX */
const galleryImages = document.querySelectorAll(".gallery img");
const lightbox = document.querySelector(".lightbox");
const lightboxImg = document.querySelector(".lightbox img");
const closeLightbox = document.querySelector(".close-lightbox");
const prevBtn = document.querySelector(".lightbox-prev");
const nextBtn = document.querySelector(".lightbox-next");

let currentImage = 0;

function openLightbox(index) {
  currentImage = index;
  lightboxImg.src = galleryImages[currentImage].src;
  lightbox.classList.add("active");
}

function closeBox() {
  lightbox.classList.remove("active");
}

function showPrev() {
  currentImage = currentImage - 1;

  if (currentImage < 0) {
    currentImage = galleryImages.length - 1;
  }

  lightboxImg.src = galleryImages[currentImage].src;
}

function showNext() {
  currentImage = currentImage + 1;

  if (currentImage >= galleryImages.length) {
    currentImage = 0;
  }

  lightboxImg.src = galleryImages[currentImage].src;
}

galleryImages.forEach((img, index) => {
  img.addEventListener("click", () => {
    openLightbox(index);
  });
});

if (closeLightbox) {
  closeLightbox.addEventListener("click", closeBox);
}

if (prevBtn) {
  prevBtn.addEventListener("click", e => {
    e.stopPropagation();
    showPrev();
  });
}

if (nextBtn) {
  nextBtn.addEventListener("click", e => {
    e.stopPropagation();
    showNext();
  });
}

if (lightbox) {
  lightbox.addEventListener("click", e => {
    if (e.target === lightbox) {
      closeBox();
    }
  });
}

document.addEventListener("keydown", e => {
  if (!lightbox || !lightbox.classList.contains("active")) return;

  if (e.key === "Escape") closeBox();
  if (e.key === "ArrowLeft") showPrev();
  if (e.key === "ArrowRight") showNext();
});

/* BACK TO TOP */
const backTop = document.querySelector(".back-top");

if (backTop) {
  backTop.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });
}