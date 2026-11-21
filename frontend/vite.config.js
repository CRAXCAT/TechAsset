import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// El puerto se fija en 5173 porque es el origen permitido por la política CORS de la API.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
  },
})
