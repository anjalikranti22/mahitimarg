---
description: MahitiMarg i18n Master Workflow - Centralized Dictionary Approach
---

# MahitiMarg i18n Master Skill
This document outlines the standard operating procedure for handling multi-language support on MahitiMarg.

## Overview
MahitiMarg supports Dual-Language navigation (`mr` and `en`) without duplicating HTML/UI structures. We achieve this by extracting all hardcoded text into a **Centralized Dictionary** (`src/i18n/ui.ts`) and rendering localized text dynamically based on the current page's locale.

## Core Rules
1. **Never Hardcode Marathi/English Text in Shared Components:**
   Always use the `useTranslations` utility to fetch text.
   ```js
   import { getLangFromUrl, useTranslations } from '../i18n/utils';
   const lang = getLangFromUrl(Astro.url);
   const t = useTranslations(lang);
   ```

2. **File Structure for Routing:**
   The `src/pages/` directory dictates the URLs (`/` for Marathi, `/en/` for English).
   However, do NOT duplicate the entire HTML inside both files.
   Instead, create a generic component (e.g., `src/components/pages/HomePage.astro`), and import it into both routing pages.
   
   *Example `src/pages/en/index.astro`:*
   ```astro
   ---
   import HomePage from '../../components/pages/HomePage.astro';
   ---
   <HomePage />
   ```

3. **Dictionary Structure (`src/i18n/ui.ts`):**
   ```typescript
   export const languages = {
     en: 'English',
     mr: 'मराठी',
   };

   export const defaultLang = 'mr';

   export const ui = {
     mr: {
       'nav.home': 'मुख्यपृष्ठ',
     },
     en: {
       'nav.home': 'Home',
     },
   } as const;
   ```

4. **SEO & Meta Tags:**
   Always pass the locale-specific `title` and `canonical` URL to the `Layout` component dynamically. Ensure `<head>` contains `<link rel="alternate" hreflang="...">` tags (handled by default in `Layout.astro`).

## Translation Automation Script
To quickly convert large hardcoded pages, an automation script (`scripts/translate-ui.js`) is maintained to extract text nodes into the Dictionary and replace them with `{t('key')}`. Run this carefully, as Astro/JSX can sometimes break. Manual refinement is always required.
