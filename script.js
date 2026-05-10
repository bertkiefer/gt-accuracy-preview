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
