/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3949AB',    // Indigo (für Hauptelemente)
        secondary: '#4CAF50',  // Grün (für Natur/Outdoor-Themen)
        accent: '#FF9800',     // Orange (als Akzentfarbe)
      }
    },
  },
  plugins: [],
}
