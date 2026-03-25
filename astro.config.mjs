import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import tailwind from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://mahitimarg.in',
  integrations: [sitemap(), mdx()],
  vite: {
    plugins: [tailwind()],
  },
});