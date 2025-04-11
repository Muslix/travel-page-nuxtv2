// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    '@nuxt/image', 
    '@nuxt/scripts', 
    '@nuxt/icon',
    '@nuxtjs/tailwindcss'
  ],
  css: [
    'vuetify/lib/styles/main.sass',
    '@mdi/font/css/materialdesignicons.min.css',
  ],
  build: {
    transpile: ['vuetify'],
  },
  vite: {
    css: {
      preprocessorOptions: {
        sass: {
          additionalData: '@use "sass:math"\n'
        }
      }
    }
  },
  app: {
    head: {
      title: 'Schwob aufm Sattl - Bikepacking & Reise-Blog',
      meta: [
        { name: 'description', content: 'Ein Blog über Bikepacking, Radreisen und Outdoor-Abenteuer' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000'
    }
  }
})