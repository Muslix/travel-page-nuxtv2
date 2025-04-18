<template>
  <v-btn
    :icon="isDarkMode ? 'mdi-weather-night' : 'mdi-weather-sunny'"
    variant="text"
    @click="toggleTheme"
    :color="isDarkMode ? 'amber-lighten-1' : 'amber-darken-3'"
    density="comfortable"
    :title="isDarkMode ? 'Zum hellen Modus wechseln' : 'Zum dunklen Modus wechseln'"
  ></v-btn>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useTheme } from 'vuetify';

const theme = useTheme();
const isDarkMode = ref(false);

// Dark Mode umschalten
function toggleTheme() {
  isDarkMode.value = !isDarkMode.value;
  theme.global.name.value = isDarkMode.value ? 'dark' : 'light';
  localStorage.setItem('darkMode', isDarkMode.value.toString());
}

// Beim Laden der Komponente den gespeicherten Theme-Zustand abrufen
onMounted(() => {
  const savedTheme = localStorage.getItem('darkMode');
  
  // Gespeicherten Theme-Zustand verwenden oder System-Präferenz prüfen
  if (savedTheme !== null) {
    isDarkMode.value = savedTheme === 'true';
  } else {
    // Prüfe System-Präferenz
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    isDarkMode.value = prefersDarkMode;
  }
  
  // Theme anwenden
  theme.global.name.value = isDarkMode.value ? 'dark' : 'light';
});

// Theme zurücksetzen wenn Seite neu geladen wird
watch(isDarkMode, (newVal) => {
  document.documentElement.classList.toggle('dark-theme', newVal);
});
</script>
