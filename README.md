# GT Accuracy — Homepage Redesign Preview

A concept redesign of [gtaccuracy.com](https://gtaccuracy.com) for Greg Taylor's
custom rifle shop in Wyalusing, PA.

**Live preview:** https://bertkiefer.github.io/gt-accuracy-preview/

## What's here

A single-page cinematic homepage built around GT Accuracy's existing brand:

- Hero with parallax/Ken-Burns and dual CTAs
- Stats bar (years, tolerance, machinery)
- Shop story / Greg's story
- Four discipline cards: Benchrest / F-Class / Hunting / Varmint
- Featured components grid
- Services list (8 in-house gunsmithing services)
- Testimonial quotes
- Visit section with embedded Google Map
- Footer

## Tech

- Plain HTML / CSS / JS (no framework, no build step)
- Brothers Bold for display, Inter for body
- Brand colors: brown, deep bronze, tan, cream
- Responsive down to mobile
- IntersectionObserver scroll-reveal

## Running locally

```bash
open index.html
```

Or any static-file server:

```bash
python3 -m http.server 8000
```

## Notes

- Photography is pulled from gtaccuracy.com — replace with higher-res versions for production.
- This is a design preview. Stripe / cart / shop functionality not wired.
- Colors and typography follow the GT Accuracy brand identity guide.
