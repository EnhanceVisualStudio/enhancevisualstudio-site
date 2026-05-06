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

const galleryImages = document.querySelectorAll(".gallery img");

let currentIndex = 0;

galleryImages.forEach((img, index) => {
  img.addEventListener("click", () => {
    currentIndex = index;
    showImage();
    lightbox.classList.add("active");
  });
});

function showImage() {
  lightboxImg.src = galleryImages[currentIndex].src;
}

closeLightbox.addEventListener("click", () => {
  lightbox.classList.remove("active");
});

lightbox.addEventListener("click", e => {
  if (e.target === lightbox) {
    lightbox.classList.remove("active");
  }
});

/* LEFT RIGHT BUTTONS */
const prevBtn = document.querySelector(".prev-btn");
const nextBtn = document.querySelector(".next-btn");

if (prevBtn && nextBtn) {

  prevBtn.addEventListener("click", () => {
    currentIndex--;

    if (currentIndex < 0) {
      currentIndex = galleryImages.length - 1;
    }

    showImage();
  });

  nextBtn.addEventListener("click", () => {
    currentIndex++;

    if (currentIndex >= galleryImages.length) {
      currentIndex = 0;
    }

    showImage();
  });
}

/* KEYBOARD */
document.addEventListener("keydown", e => {

  if (!lightbox.classList.contains("active")) return;

  if (e.key === "Escape") {
    lightbox.classList.remove("active");
  }

  if (e.key === "ArrowRight") {
    currentIndex++;

    if (currentIndex >= galleryImages.length) {
      currentIndex = 0;
    }

    showImage();
  }

  if (e.key === "ArrowLeft") {
    currentIndex--;

    if (currentIndex < 0) {
      currentIndex = galleryImages.length - 1;
    }

    showImage();
  }

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