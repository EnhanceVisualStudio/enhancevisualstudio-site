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
  if (!lightbox || !lightboxImg || !galleryImages.length) return;

  currentImage = index;
  lightboxImg.src = galleryImages[currentImage].src;
  lightbox.classList.add("active");
}

function closeBox() {
  if (!lightbox) return;
  lightbox.classList.remove("active");
}

function showPrev() {
  if (!lightboxImg || !galleryImages.length) return;

  currentImage--;

  if (currentImage < 0) {
    currentImage = galleryImages.length - 1;
  }

  lightboxImg.src = galleryImages[currentImage].src;
}

function showNext() {
  if (!lightboxImg || !galleryImages.length) return;

  currentImage++;

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
/* SWIPE LEFT / RIGHT IN LIGHTBOX */
let touchStartX = 0;
let touchEndX = 0;

if (lightbox) {
  lightbox.addEventListener("touchstart", e => {
    touchStartX = e.changedTouches[0].screenX;
  });

  lightbox.addEventListener("touchend", e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  });
}

function handleSwipe() {
  const swipeDistance = touchEndX - touchStartX;

  if (Math.abs(swipeDistance) < 50) return;

  if (swipeDistance < 0) {
    showNext();
  }

  if (swipeDistance > 0) {
    showPrev();
  }
}