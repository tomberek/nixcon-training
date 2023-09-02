import { defineConfig } from 'astro/config';

const port = process.env["PORT"]

// https://astro.build/config
export default defineConfig({
  server: {
      port: Number(port)
  },
  // ...
  vite: {
    server: {
      proxy: {
        "/api": {
          target: `http://127.0.0.1:${Number(port) + 100}/`,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
  },
});
