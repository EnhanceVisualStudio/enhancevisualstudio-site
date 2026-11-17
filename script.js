import { catalog } from "./assets/booking-catalog.mjs";

const menu = document.querySelector(".menu-button");
const navigation = document.querySelector("#site-nav");
const narrowScreen = matchMedia("(max-width: 900px)");

function setMenu(open) {
  navigation.hidden = narrowScreen.matches && !open;
  menu.setAttribute("aria-expanded", String(open));
}

function syncMenu() {
  if (narrowScreen.matches && navigation.contains(document.activeElement)) menu.focus();
  if (!narrowScreen.matches && document.activeElement === menu) navigation.querySelector("a").focus();
  setMenu(false);
}

menu.hidden = false;
syncMenu();
narrowScreen.addEventListener("change", syncMenu);
menu.addEventListener("click", () => setMenu(menu.getAttribute("aria-expanded") === "false"));

const params = new URLSearchParams(location.search);
const filterBar = document.querySelector("#gallery-filters");

if (filterBar) {
  const gallery = document.querySelector("#gallery");
  const figures = [...gallery.querySelectorAll("figure")];
  const filters = [...filterBar.querySelectorAll("[data-filter]")];
  const counter = document.querySelector("#gallery-count");
  const lightbox = document.querySelector(".lightbox");
  const photo = lightbox.querySelector("img");
  const photoCount = lightbox.querySelector(".lightbox-count");
  let visible = [];
  let index = 0;
  let opener;

  function filter(category) {
    filters.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.filter === category)));
    figures.forEach((figure) => {
      figure.hidden = category !== "all" && !figure.dataset.categories.split(" ").includes(category);
    });
    visible = figures.filter((figure) => !figure.hidden).map((figure) => figure.querySelector("a"));
    counter.textContent = visible.length === 1 ? "1 photograph" : visible.length + " photographs";
  }

  function updatePhoto(next) {
    index = (next + visible.length) % visible.length;
    const link = visible[index];
    photo.alt = link.querySelector("img").alt;
    photo.src = link.href;
    photoCount.textContent = (index + 1) + " of " + visible.length;
  }

  filterBar.hidden = false;
  const requested = params.get("category");
  filter(filters.some((button) => button.dataset.filter === requested) ? requested : "all");
  filterBar.addEventListener("click", (event) => {
    const button = event.target.closest("[data-filter]");
    if (button) filter(button.dataset.filter);
  });

  if (typeof lightbox.showModal === "function") {
    const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");
    photo.addEventListener("load", () => {
      if (lightbox.open && !reduceMotion.matches) {
        photo.animate([{ opacity: 0.55 }, { opacity: 1 }], { duration: 220, easing: "ease-out" });
      }
    });
    gallery.addEventListener("click", (event) => {
      const link = event.target.closest(".gallery-image");
      if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      updatePhoto(visible.indexOf(link));
      lightbox.showModal();
    });
    lightbox.addEventListener("click", (event) => {
      if (event.target.closest(".lightbox-close")) lightbox.close();
      const button = event.target.closest("[data-advance]");
      if (button) updatePhoto(index + Number(button.dataset.advance));
    });
    lightbox.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
      event.preventDefault();
      updatePhoto(index + (event.key === "ArrowLeft" ? -1 : 1));
    });
    lightbox.addEventListener("close", () => {
      photo.removeAttribute("src");
      opener.focus({ preventScroll: true });
    });
  }
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !document.querySelector("dialog[open]") &&
      narrowScreen.matches && menu.getAttribute("aria-expanded") === "true") {
    setMenu(false);
    menu.focus();
  }
});

const form = document.querySelector(".request-form");

if (form) {
  const service = form.elements.namedItem("service");
  const packageField = form.elements.namedItem("package");
  const status = form.querySelector(".form-status");
  const submit = form.querySelector('button[type="submit"]');

  function syncPackages() {
    const available = catalog.packageServices[service.value] || [];
    for (const option of packageField.options) {
      option.disabled = option.value !== "custom" && !available.includes(option.value);
    }
    if (packageField.selectedOptions[0]?.disabled) packageField.value = "custom";
  }

  const requestedService = params.get("service");
  const requestedPackage = params.get("package");
  if (Object.hasOwn(catalog.services, requestedService)) service.value = requestedService;

  if (packageField) {
    if (Object.hasOwn(catalog.packages, requestedPackage)) {
      if (requestedPackage !== "custom" && !service.value) {
        service.value = requestedPackage === "creative-campaign" ? "branding" : "portraits";
      }
      packageField.value = requestedPackage;
    }
    syncPackages();
    service.addEventListener("change", syncPackages);

    const todayParts = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Los_Angeles", year: "numeric", month: "2-digit", day: "2-digit",
    }).formatToParts(new Date());
    const parts = Object.fromEntries(todayParts.map(({ type, value }) => [type, value]));
    for (const name of ["preferredDate", "alternateDate"]) {
      form.elements.namedItem(name).min = parts.year + "-" + parts.month + "-" + parts.day;
    }
  }

  form.hidden = false;
  const fallback = "Your request could not be confirmed. Please try again or email hello@enhancevisualstudio.com.";

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (submit.disabled) return;
    const data = Object.fromEntries(new FormData(form));
    data.kind = form.dataset.kind;
    submit.disabled = true;
    delete status.dataset.state;
    status.textContent = "Sending your request…";

    try {
      const response = await fetch("/api/inquiry", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data),
        credentials: "omit",
      });
      const result = await response.json();
      if (!response.ok || result.ok !== true || typeof result.message !== "string") {
        throw new Error(typeof result.error === "string" ? result.error : fallback);
      }
      form.reset();
      if (packageField) syncPackages();
      status.textContent = result.message;
    } catch (error) {
      status.dataset.state = "error";
      status.textContent = error.name === "SyntaxError" || error instanceof TypeError ? fallback : error.message;
    } finally {
      submit.disabled = false;
    }
  });
}
