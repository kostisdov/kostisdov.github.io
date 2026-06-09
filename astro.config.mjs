import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  // Set this to your real domain (or https://<user>.github.io) before deploying.
  site: 'https://kostisdovelos.com',
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
    shikiConfig: {
      theme: 'vitesse-light',
    },
  },
});
