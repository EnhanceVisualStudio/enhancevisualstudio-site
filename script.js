const menuBtn = document.querySelector(".menu-btn");
const nav = document.querySelector(".nav");

/* MOBILE MENU */
if (menuBtn && nav) {
  menuBtn.addEventListener("click", () => {
    nav.classList.toggle("active");
  });
}

/* LOADER */
const loader = document.querySelector(".loader");

window.addEventListener("load", () => {
  if (loader) {
    loader.classList.add("hidden");
  }
});

/* PORTFOLIO IMAGE REVEAL + ZOOM */
const galleryImages = document.querySelectorAll(".gallery img");

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
    }
  });
}, {
  threshold: 0.15
});

galleryImages.forEach(img => {
  observer.observe(img);
});

/* LIGHTBOX */
const lightbox = document.querySelector(".lightbox");
const lightboxImg = document.querySelector(".lightbox img");

let currentIndex = 0;

function openLightbox(index) {
  currentIndex = index;
  lightboxImg.src = galleryImages[currentIndex].src;
  lightbox.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeLightbox() {
  lightbox.classList.remove("active");
  document.body.style.overflow = "auto";
}

function showNext() {
  currentIndex = (currentIndex + 1) % galleryImages.length;
  lightboxImg.src = galleryImages[currentIndex].src;
}

function showPrev() {
  currentIndex = (currentIndex - 1 + galleryImages.length) % galleryImages.length;
  lightboxImg.src = galleryImages[currentIndex].src;
}

galleryImages.forEach((img, index) => {
  img.addEventListener("click", () => {
    openLightbox(index);
  });
});

/* CLOSE BUTTON */
const closeBtn = document.querySelector(".close-lightbox");

if (closeBtn) {
  closeBtn.addEventListener("click", closeLightbox);
}

/* ARROWS */
const nextBtn = document.querySelector(".next-image");
const prevBtn = document.querySelector(".prev-image");

if (nextBtn) {
  nextBtn.addEventListener("click", showNext);
}

if (prevBtn) {
  prevBtn.addEventListener("click", showPrev);
}

/* ESC KEY */
document.addEventListener("keydown", (e) => {
  if (!lightbox) return;

  if (e.key === "Escape") {
    closeLightbox();
  }

  if (e.key === "ArrowRight") {
    showNext();
  }

  if (e.key === "ArrowLeft") {
    showPrev();
  }
});

/* CLICK OUTSIDE IMAGE */
if (lightbox) {
  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) {
      closeLightbox();
    }
  });
}

/* RETURN TO TOP */
const topBtn = document.querySelector(".return-top");

if (topBtn) {
  topBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });
}