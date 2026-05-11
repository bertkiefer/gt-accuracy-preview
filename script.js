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
