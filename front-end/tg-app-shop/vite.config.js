import { fileURLToPath, URL } from 'node:url'
import path from 'path'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [
      vue(),
      VueDevTools(),
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
        'localhost',
        '*.twc1.net',
        'all',
        'mms021-six-shop-f408.twc1.net',
      ],
      proxy: {
        '/static': {
          target:  'http://localhost:7770',
          changeOrigin: true,
        }
      }
    }
  }
})
