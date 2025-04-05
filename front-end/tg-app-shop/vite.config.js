import { fileURLToPath, URL } from 'node:url'
import path from 'path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    //VueDevTools(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    }
  },
  server: {
    host: '0.0.0.0',
    port: 3478,
    allowedHosts: [ 
      process.env.VITE_API_BASE_URL,
      process.env.VITE_STATIC_URL
    ],

    proxy: {
      '/static': {
        target: process.env.VITE_API_BASE_URL,
        changeOrigin: true,
      }
    }
  }
})
