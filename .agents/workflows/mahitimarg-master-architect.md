---
description: The complete master skill for building mahitimarg.in using Astro. Enforces high-end GSAP UI, strict SEO schema, interactive filtering, traffic funneling from satellite tools, and AdSense-ready CLS protection.
---

# MahitiMarg Master Standards (Astro + UI + SEO + Monetization)

## 1. GSAP & SEO Master Standards (The "SEO-First" Rule)
- **Astro Server-Side Rendering:** Never hide DOM elements from crawlers. Do not use `display: none` or render empty divs that are populated later by JavaScript. All Marathi text, scheme titles, and links must be fully present in the SSR HTML.
- **Animate via CSS Transforms:** Only animate `transform` (scale, translate) and `opacity`. This ensures the animation is handled by the GPU and prevents expensive browser repaints that ruin Core Web Vitals.
- **Bento-Box & Glassmorphism:** Default to a "Bento-Box" CSS Grid layout for displaying Yojana categories and smart tools. Apply subtle glassmorphism to cards: `bg-white/80`, `backdrop-blur-md`, and a light border `border-white/20`.
- **Typography (Marathi):** Always use the **Mukta** font family for Marathi text. Enforce a `line-height` of at least `1.6` for readability and ensure heading tags (`<h1>`, `<h2>`) are strictly semantic.
- **GSAP Scroll & Hover:** Use GSAP ScrollTrigger for staggered entrances (`y: 40` to `0`, `opacity: 0` to `1`). When a user hovers over a card, use GSAP to smoothly scale to `1.03`. Always wrap animations in a `prefers-reduced-motion` media query check.
- **Semantic Schema:** Whenever generating a component detailing a government scheme, automatically wrap content in semantic HTML (`<article>`) and include standard JSON-LD `GovernmentService` and `FAQPage` schema markup in the `<head>`.

## 2. Interactive UI & Feedback Standards
- **The "Tactile Touch" Rule:** Every clickable element (category chips, tools, buttons) must have a distinct `:active` CSS state (e.g., `active:scale-95`) to simulate a physical button press.
- **Focus Rings:** Ensure high-contrast, offset outlines for keyboard navigation (`focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`).
- **Astro View Transitions:** Always utilize Astro's `<ViewTransitions />` router. Filtering schemes by Category, Income, or Age must cross-fade or slide smoothly without a hard page refresh.
- **Skeleton Loaders & Empty States:** Use shimmering CSS gradients (`animate-pulse`) while waiting for search results. If a search yields zero results, render a friendly SVG graphic and suggest two default popular schemes.
- **Floating Labels:** All text inputs (like the main scheme search) must use the floating label pattern, transitioning the placeholder into a top-left label on focus.

## 3. Traffic Funneling & Tool Integration Standards
- **The "Soft Handoff" Rule (No Auto-Redirects):** Never force an automatic redirect after a user completes a calculation on satellite sites (like the pahsky calculator) or internal tools. 
- **Contextual CTAs:** Render a highly visible Call-to-Action card below the tool result. (e.g., "तुम्ही या योजनेसाठी पात्र आहात! संपूर्ण माहिती वाचण्यासाठी येथे क्लिक करा." - You are eligible! Click here to read full details).
- **State Preservation:** Pass user input data via URL parameters (e.g., `?income=low`) when clicking the CTA. The destination article should highlight the specific paragraphs relevant to that user's input.
- **Inline Smart Tools:** Embed mini-versions of relevant calculators halfway down long-form `<article>` pages to maintain engagement.

## 4. Ad Placement & CLS Protection Standards
- **Strict CLS Prevention (Zero-Jank Layouts):** To prepare for AdSense approval, reserve ad slots. Force the creation of skeleton wrapper `<div>` tags with explicit AdSense dimensions (e.g., `min-h-[250px] w-full`).
- **Placeholder Styling:** Give these reserved slots subtle styling (`bg-slate-50 border border-dashed border-slate-200`) so they blend in before ads load, preventing layout jumping.
- **Unintrusive Ad Positioning:** Never place an ad wrapper inside the first 500 words of a critical Yojana article. Place the first ad wrapper *after* the initial summary and eligibility criteria.
- **Sticky Sidebars:** Use `position: sticky` on desktop sidebars for ad wrappers so they remain in view as the user scrolls through long Marathi content.
