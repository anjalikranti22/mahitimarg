import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import tailwind from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://mahitimarg.in',
  integrations: [sitemap(), mdx()],
  i18n: {
    defaultLocale: "mr",
    locales: ["mr", "en"],
    routing: {
      prefixDefaultLocale: false,
    }
  },
  vite: {
    plugins: [tailwind()],
  },
});