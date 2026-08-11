import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './',
  server: {
    port: 5173,
    // Proxy de desarrollo: evita CORS pegandole al backend de Render.
    // Para usarlo, deja VITE_API_URL vacia y el front llamara a /api/... local.
    proxy: {
      '/api': {
        target: 'https://energiai-backend-g68o.onrender.com',
        changeOrigin: true,
        secure: true,
      },
    },
  },
})
