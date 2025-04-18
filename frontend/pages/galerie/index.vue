<template>
  <div>
    <!-- Hero-Banner für Galerie -->
    <div class="gallery-hero relative">
      <v-img
        src="https://images.unsplash.com/photo-1486435286105-07c4f9544d85?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3540&q=80"
        height="400"
        cover
        :class="{'darken-image-in-dark-mode': isDarkMode}"
      >
        <div class="absolute inset-0 bg-gradient-to-b from-black/50 to-black/70 flex items-center">
          <v-container>
            <h1 class="text-h2 font-weight-bold text-white mb-4">Galerie</h1>
            <p class="text-h6 text-white max-w-lg">
              Eindrücke und Momente von meinen Bikepacking-Abenteuern
            </p>
          </v-container>
        </div>
      </v-img>
    </div>

    <v-container class="py-12">
      <!-- Filter-Optionen -->
      <v-row class="mb-8">
        <v-col cols="12" md="6">
          <h2 class="text-h4 font-weight-bold mb-2">Abenteuer in Bildern</h2>
          <p class="text-subtitle-1">Eindrucksvolle Momente von meinen Radreisen</p>
        </v-col>
        <v-col cols="12" md="6" class="d-flex flex-wrap gap-2 align-center justify-end">
          <v-chip-group
            v-model="selectedFilter"
            mandatory
            selected-class="bg-primary text-white"
            @update:modelValue="filterImages"
          >
            <v-chip value="alle">Alle</v-chip>
            <v-chip value="landschaften">Landschaften</v-chip>
            <v-chip value="fahrrad">Fahrrad</v-chip>
            <v-chip value="camping">Camping</v-chip>
            <v-chip value="menschen">Menschen</v-chip>
            <v-chip value="strassen">Straßen</v-chip>
          </v-chip-group>
        </v-col>
      </v-row>

      <!-- Loading, Error und Empty States -->
      <div v-if="isLoading" class="d-flex justify-center my-12">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </div>
      
      <div v-else-if="error" class="text-center my-12">
        <v-alert type="error" title="Fehler beim Laden" :text="error.message"></v-alert>
        <v-btn color="primary" class="mt-6" @click="loadImages">Erneut versuchen</v-btn>
      </div>
      
      <div v-else-if="images.length === 0" class="text-center my-12">
        <v-alert type="info" title="Keine Bilder" text="Es wurden noch keine Bilder in der Galerie veröffentlicht."></v-alert>
      </div>
      
      <!-- Masonry Gallery Layout -->
      <div v-else>
        <v-row>
          <v-col 
            v-for="(image, index) in displayedImages" 
            :key="image.id" 
            cols="12" sm="6" md="4"
            class="gallery-item"
          >
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                class="gallery-card"
                :elevation="isHovering ? 8 : 2"
                @click="openLightbox(index)"
              >
                <v-img
                  :src="image.url"
                  :aspect-ratio="image.aspectRatio || 1"
                  cover
                  class="gallery-image"
                >
                  <template v-slot:placeholder>
                    <v-row class="fill-height ma-0" align="center" justify="center">
                      <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    </v-row>
                  </template>
                  
                  <div v-if="isHovering" class="image-overlay d-flex align-center justify-center">
                    <v-btn icon="mdi-magnify" color="white" size="large" variant="text"></v-btn>
                  </div>
                </v-img>
                
                <v-card-text class="pa-3">
                  <p class="text-subtitle-2 font-weight-bold mb-1">{{ image.title }}</p>
                  <p class="text-caption text-medium-emphasis">{{ image.location }}</p>
                </v-card-text>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
        
        <!-- Load More Button -->
        <div v-if="hasMoreImages" class="text-center mt-8">
          <v-btn 
            color="primary" 
            variant="outlined" 
            size="large"
            :loading="isLoadingMore"
            @click="loadMoreImages"
          >
            Mehr laden
          </v-btn>
        </div>
      </div>
    </v-container>
    
    <!-- Lightbox -->
    <v-dialog
      v-model="lightbox.show"
      fullscreen
      transition="dialog-bottom-transition"
      :scrim="false"
    >
      <v-card class="lightbox-container">
        <v-toolbar color="black" density="compact">
          <v-spacer></v-spacer>
          <v-btn icon="mdi-close" color="white" variant="text" @click="lightbox.show = false"></v-btn>
        </v-toolbar>
        
        <v-container fluid class="fill-height pa-0">
          <v-row class="fill-height ma-0">
            <v-col cols="12" class="d-flex flex-column justify-center align-center pa-0">
              <div class="lightbox-controls d-flex align-center justify-space-between w-100">
                <v-btn 
                  icon="mdi-chevron-left" 
                  color="white" 
                  size="x-large" 
                  variant="text"
                  :disabled="lightbox.index <= 0"
                  @click="prevImage"
                ></v-btn>
                
                <v-img
                  :src="currentLightboxImage?.url"
                  max-height="90vh"
                  contain
                  class="lightbox-image"
                ></v-img>
                
                <v-btn 
                  icon="mdi-chevron-right" 
                  color="white" 
                  size="x-large" 
                  variant="text"
                  :disabled="lightbox.index >= displayedImages.length - 1"
                  @click="nextImage"
                ></v-btn>
              </div>
              
              <div class="lightbox-info text-center mt-4">
                <p class="text-h6 text-white mb-1">{{ currentLightboxImage?.title }}</p>
                <p class="text-subtitle-2 text-grey">{{ currentLightboxImage?.description }}</p>
                <p class="text-caption text-grey-lighten-1 mt-2">
                  <v-icon size="small" class="mr-1">mdi-map-marker</v-icon>
                  {{ currentLightboxImage?.location }}
                </p>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useTheme } from 'vuetify';

const theme = useTheme();
const isDarkMode = computed(() => theme.global.current.value.dark);

// Galerie-Zustand
const isLoading = ref(true);
const error = ref<Error | null>(null);
const images = ref<any[]>([]);
const displayedImages = ref<any[]>([]);
const selectedFilter = ref('alle');
const page = ref(1);
const limit = ref(12);
const isLoadingMore = ref(false);
const hasMoreImages = ref(true);

// Lightbox-Zustand
const lightbox = ref({
  show: false,
  index: 0
});

const currentLightboxImage = computed(() => {
  if (lightbox.value.index >= 0 && lightbox.value.index < displayedImages.value.length) {
    return displayedImages.value[lightbox.value.index];
  }
  return null;
});

// Dummy-Daten für die Galerie (in einem echten Projekt würden diese von einer API kommen)
function generateDummyImages() {
  const categories = ['landschaften', 'fahrrad', 'camping', 'menschen', 'strassen'];
  const locations = ['Schwarzwald', 'Allgäu', 'Alpen', 'Bodensee', 'Schwäbische Alb', 'Bayern'];
  
  const dummyImages = [];
  
  for (let i = 1; i <= 30; i++) {
    // Zufällige Kategorie und Standort
    const categoryIndex = Math.floor(Math.random() * categories.length);
    const locationIndex = Math.floor(Math.random() * locations.length);
    
    // Zufälliges Seitenverhältnis für abwechslungsreiches Layout
    const aspectRatios = [1, 4/3, 3/4, 16/9, 9/16];
    const aspectRatioIndex = Math.floor(Math.random() * aspectRatios.length);
    
    dummyImages.push({
      id: i,
      title: `Bikepacking Bild ${i}`,
      description: `Beschreibung des Bildes ${i} von einer Bikepacking-Tour.`,
      url: `https://picsum.photos/seed/${i}/800/600`,
      category: categories[categoryIndex],
      location: locations[locationIndex],
      aspectRatio: aspectRatios[aspectRatioIndex]
    });
  }
  
  return dummyImages;
}

// Bilder laden
function loadImages() {
  isLoading.value = true;
  error.value = null;
  
  try {
    // Hier würde normalerweise ein API-Aufruf erfolgen
    // In diesem Beispiel verwenden wir Dummy-Daten
    setTimeout(() => {
      images.value = generateDummyImages();
      filterImages();
      isLoading.value = false;
    }, 1000);
  } catch (err) {
    error.value = err as Error;
    isLoading.value = false;
  }
}

// Bilder nach Kategorie filtern
function filterImages() {
  if (selectedFilter.value === 'alle') {
    // Alle Bilder anzeigen
    displayedImages.value = images.value.slice(0, page.value * limit.value);
  } else {
    // Nach Kategorie filtern
    const filtered = images.value.filter(img => img.category === selectedFilter.value);
    displayedImages.value = filtered.slice(0, page.value * limit.value);
  }
  
  // Prüfen, ob es weitere Bilder gibt
  const totalFilteredImages = selectedFilter.value === 'alle' 
    ? images.value.length 
    : images.value.filter(img => img.category === selectedFilter.value).length;
    
  hasMoreImages.value = displayedImages.value.length < totalFilteredImages;
}

// Weitere Bilder laden
function loadMoreImages() {
  isLoadingMore.value = true;
  
  setTimeout(() => {
    page.value++;
    filterImages();
    isLoadingMore.value = false;
  }, 800);
}

// Lightbox öffnen
function openLightbox(index: number) {
  lightbox.value.index = index;
  lightbox.value.show = true;
}

// Zum vorherigen Bild
function prevImage() {
  if (lightbox.value.index > 0) {
    lightbox.value.index--;
  }
}

// Zum nächsten Bild
function nextImage() {
  if (lightbox.value.index < displayedImages.value.length - 1) {
    lightbox.value.index++;
  }
}

// Bilder beim Mounten der Komponente laden
onMounted(() => {
  loadImages();
});

// Seitentitel und Meta-Tags
useHead({
  title: 'Galerie | Schwob aufm Sattl',
  meta: [
    {
      name: 'description',
      content: 'Galerie mit Eindrücken und Bildern von Bikepacking-Abenteuern und Radreisen'
    }
  ]
});
</script>

<style scoped>
.gallery-card {
  transition: all 0.3s;
  cursor: pointer;
  overflow: hidden;
}

.gallery-image {
  transition: transform 0.3s ease;
}

.gallery-card:hover .gallery-image {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  transition: opacity 0.3s;
}

.lightbox-container {
  background-color: rgba(0, 0, 0, 0.95);
}

.lightbox-controls {
  position: relative;
  padding: 0 24px;
}

.lightbox-image {
  max-width: 90vw;
}

.darken-image-in-dark-mode {
  filter: brightness(0.8);
}
</style>
