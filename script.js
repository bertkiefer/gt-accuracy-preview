try { sessionStorage.removeItem("quoteCtaDismissed"); } catch(e) {}
// Scroll-reveal: add .in to .reveal sections as they enter the viewport
const observer = new IntersectionObserver(
  entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        observer.unobserve(e.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: "0px 0px -10% 0px" }
);
document.querySelectorAll(".reveal").forEach(el => observer.observe(el));

// Quote CTA: slides in from bottom-right after the user scrolls past the hero,
// has a one-time attention pulse, and can be dismissed for this page view only
// (any reload brings it back — important for a pitch/demo site).
(() => {
  const cta = document.querySelector(".quote-cta");
  if (!cta) return;

  const closeBtn = cta.querySelector(".quote-cta-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", e => {
      e.preventDefault();
      cta.classList.remove("in", "pulse");
      cta.classList.add("dismissed");
    });
  }

  let shown = false;
  const threshold = Math.min(600, window.innerHeight * 0.6);
  function onScroll() {
    if (shown) return;
    if (window.scrollY > threshold) {
      shown = true;
      cta.classList.add("in");
      // Pulse twice after entry to draw the eye
      setTimeout(() => cta.classList.add("pulse"), 700);
      setTimeout(() => cta.classList.remove("pulse"), 3500);
      window.removeEventListener("scroll", onScroll);
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
})();

// Contact form: required-field validation + swap to success state on submit.
// No backend wired yet — when you hook up Formspree / Netlify Forms / a Worker,
// replace this block with a real fetch().
(() => {
  const form = document.getElementById("contact-form");
  if (!form) return;
  const successEl = form.querySelector(".form-success");
  const grid = form.querySelector(".form-grid");
  const bar = form.querySelector(".form-bar");

  form.addEventListener("submit", e => {
    e.preventDefault();
    // Minimal required-field check
    const name = form.elements.name.value.trim();
    const email = form.elements.email.value.trim();
    if (!name || !email || !/.+@.+\..+/.test(email)) {
      // Briefly flash the offending fields
      [form.elements.name, form.elements.email].forEach(f => {
        if (!f.value.trim() || (f.type === "email" && !/.+@.+\..+/.test(f.value))) {
          f.style.borderColor = "#b8462f";
          setTimeout(() => { f.style.borderColor = ""; }, 1600);
        }
      });
      return;
    }
    // Swap the form body for the success state
    grid.style.display = "none";
    bar.style.display = "none";
    successEl.hidden = false;
    successEl.scrollIntoView({ behavior: "smooth", block: "center" });
  });
})();

// Match scroll-padding-top to the actual rendered nav height so anchor jumps
// always land below the sticky nav, no matter the logo size or viewport.
(() => {
  const nav = document.querySelector(".nav");
  if (!nav) return;
  function applyPad() {
    const h = nav.getBoundingClientRect().height;
    document.documentElement.style.scrollPaddingTop = (h + 16) + "px";
  }
  applyPad();
  window.addEventListener("resize", applyPad, { passive: true });
  window.addEventListener("load", applyPad);
  // Also recompute after the logo image decodes (its height drives the nav height)
  const logoImg = nav.querySelector("img");
  if (logoImg) {
    if (logoImg.complete) applyPad();
    else logoImg.addEventListener("load", applyPad);
  }
})();

// Ranch SWAG lightbox: click a swag card to open the zoomed product detail.
(() => {
  const lb       = document.getElementById("swag-lightbox");
  if (!lb) return;
  const lbImg    = document.getElementById("lb-img");
  const lbName   = document.getElementById("lb-name");
  const lbTag    = document.getElementById("lb-tag");
  const lbDesc   = document.getElementById("lb-desc");
  const lbPrice  = document.getElementById("lb-price");

  function open(card) {
    lbImg.src   = card.dataset.img;
    lbImg.alt   = card.dataset.name || "";
    lbName.textContent  = card.dataset.name  || "";
    lbTag.textContent   = (card.dataset.tag || "").toUpperCase();
    lbDesc.textContent  = card.dataset.desc  || "";
    lbPrice.textContent = card.dataset.price || "";
    lb.classList.add("open");
    lb.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }
  function close() {
    lb.classList.remove("open");
    lb.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  document.querySelectorAll(".swag-card").forEach(card => {
    card.addEventListener("click", () => open(card));
    card.setAttribute("tabindex", "0");
    card.addEventListener("keydown", e => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(card); }
    });
  });
  lb.querySelectorAll("[data-close]").forEach(el => el.addEventListener("click", close));
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && lb.classList.contains("open")) close();
  });
})();
