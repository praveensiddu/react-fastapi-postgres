import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, '../backend/static'),
    emptyOutDir: true,
  },
  server: {
    port: 3000,
    proxy: {
      '/users': 'http://localhost:8000' // Proxy API calls during dev
    }
  }
});
