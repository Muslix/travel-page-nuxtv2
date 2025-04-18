// plugins/vuetify.ts
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default defineNuxtPlugin(nuxtApp => {
  const vuetify = createVuetify({
    ssr: true,
    components,
    directives,
    theme: {
      defaultTheme: 'light',
      themes: {
        light: {
          dark: false,
          colors: {
            primary: '#3949AB',    // Indigo (für Hauptelemente)
            secondary: '#4CAF50',  // Grün (für Natur/Outdoor-Themen)
            accent: '#FF9800',     // Orange (als Akzentfarbe)
            error: '#F44336',
            warning: '#FFC107',
            info: '#2196F3',
            success: '#4CAF50'
          }
        },
        dark: {
          dark: true,
          colors: {
            primary: '#5C6BC0',    // Helleres Indigo für Dark Mode
            secondary: '#66BB6A',  // Helleres Grün für Dark Mode
            accent: '#FFA726',     // Helleres Orange für Dark Mode
            error: '#EF5350',
            warning: '#FFCA28',
            info: '#42A5F5',
            success: '#66BB6A'
          }
        }
      }
    }
  })

  nuxtApp.vueApp.use(vuetify)
})
