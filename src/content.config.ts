import { z, defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

const schemeSchema = z.object({
  title: z.string(),
  description: z.string(),
  badge: z.string(),
  apply_link: z.string().optional().nullable(),
  key_stat: z.string().optional().nullable(),
  english_title: z.string().optional().nullable(),
  keywords: z.string().optional().nullable(),
});

const schemeCollection = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/schemes" }),
  schema: schemeSchema,
});

const schemeEnCollection = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/schemes-en" }),
  schema: schemeSchema,
});

export const collections = {
  'schemes': schemeCollection,
  'schemes-en': schemeEnCollection,
};
