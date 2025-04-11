<template>
  <div>
    <div v-if="isLoading" class="my-12 d-flex justify-center">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </div>

    <div v-else-if="error" class="my-12">
      <v-alert type="error" title="Fehler beim Laden" :text="error.message"></v-alert>
      <div class="d-flex justify-center mt-6">
        <v-btn color="primary" @click="loadAdventure">Erneut versuchen</v-btn>
        <v-btn color="secondary" class="ml-4" to="/abenteuer">Zurück zur Übersicht</v-btn>
      </div>
    </div>

    <template v-else-if="adventure">
      <!-- Hero-Bild mit Titel -->
      <div class="relative">
        <v-img
          :src="adventure.featured_image_url || 'https://images.unsplash.com/photo-1473861646675-0ca14fee6856?ixlib=rb-4.0.3&auto=format&fit=crop'"
          height="500"
          cover
          class="adventure-hero"
        >
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent flex items-end">
            <v-container class="pb-8">
              <h1 class="text-h2 text-white font-weight-bold">{{ adventure.title }}</h1>
              
              <div class="d-flex align-center flex-wrap mt-4">
                <v-chip-group v-if="adventure.tags && adventure.tags.length > 0">
                  <v-chip v-for="tag in adventure.tags" :key="tag.id" color="primary" variant="outlined" class="mr-2 mb-2">
                    {{ tag.name }}
                  </v-chip>
                </v-chip-group>
              </div>
            </v-container>
          </div>
        </v-img>
      </div>

      <v-container class="py-8">
        <!-- Abenteuer-Details -->
        <v-row>
          <v-col cols="12" md="8">
            <!-- Beschreibung -->
            <div class="text-subtitle-1 mb-6">{{ adventure.description }}</div>
            
            <!-- Hauptinhalt -->
            <div class="adventure-content">
              <div v-html="adventure.content" class="prose max-w-none"></div>
            </div>
            
            <!-- Bilder-Galerie -->
            <div v-if="adventure.images && adventure.images.length > 0" class="mt-12">
              <h2 class="text-h4 mb-6">Galerie</h2>
              <v-row>
                <v-col v-for="image in adventure.images" :key="image.id" cols="12" sm="6" md="4">
                  <v-img :src="image.url" :alt="image.alt_text || adventure.title" aspect-ratio="1" class="rounded-lg"></v-img>
                </v-col>
              </v-row>
            </div>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-card class="mb-6">
              <v-card-title>Abenteuer-Details</v-card-title>
              <v-card-text>
                <div v-if="adventure.distance_km" class="d-flex align-center mb-4">
                  <v-icon color="primary" class="mr-2">mdi-map-marker-distance</v-icon>
                  <div>
                    <div class="text-body-2 text-grey">Distanz</div>
                    <div class="text-h6">{{ adventure.distance_km }} km</div>
                  </div>
                </div>
                
                <div v-if="adventure.elevation_m" class="d-flex align-center mb-4">
                  <v-icon color="primary" class="mr-2">mdi-elevation-rise</v-icon>
                  <div>
                    <div class="text-body-2 text-grey">Höhenmeter</div>
                    <div class="text-h6">{{ adventure.elevation_m }} m</div>
                  </div>
                </div>
                
                <div v-if="adventure.duration_days" class="d-flex align-center mb-4">
                  <v-icon color="primary" class="mr-2">mdi-calendar-range</v-icon>
                  <div>
                    <div class="text-body-2 text-grey">Dauer</div>
                    <div class="text-h6">{{ adventure.duration_days }} Tage</div>
                  </div>
                </div>
                
                <div v-if="adventure.difficulty" class="d-flex align-center mb-4">
                  <v-icon color="primary" class="mr-2">mdi-alert</v-icon>
                  <div>
                    <div class="text-body-2 text-grey">Schwierigkeit</div>
                    <div class="text-h6">{{ adventure.difficulty }}</div>
                  </div>
                </div>
              </v-card-text>
            </v-card>
            
            <!-- GPX Route Download -->
            <v-card v-if="adventure.route_gpx_url" class="mb-6">
              <v-card-title>GPX Route</v-card-title>
              <v-card-text>
                <p>Lade die GPX-Route für dein GPS-Gerät oder Smartphone herunter.</p>
              </v-card-text>
              <v-card-actions>
                <v-btn block color="primary" :href="adventure.route_gpx_url" target="_blank">
                  <v-icon left>mdi-download</v-icon>
                  GPX herunterladen
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import useAdventureService from '~/services/adventure-service';
import type { Adventure } from '~/types/adventure';

const route = useRoute();
const adventureSlug = route.params.slug as string;

const adventure = ref<Adventure | null>(null);
const isLoading = ref(true);
const error = ref<Error | null>(null);

const adventureService = useAdventureService();

async function loadAdventure() {
  isLoading.value = true;
  error.value = null;
  
  try {
    const { adventure: loadedAdventure, error: loadError } = await adventureService.getAdventureBySlug(adventureSlug);
    
    if (loadError) {
      error.value = loadError as Error;
    } else {
      adventure.value = loadedAdventure;
    }
  } catch (err) {
    console.error('Failed to load adventure:', err);
    error.value = err as Error;
  } finally {
    isLoading.value = false;
  }
}

onMounted(async () => {
  await loadAdventure();
});
</script>

<style>
.adventure-hero {
  position: relative;
}

.adventure-content {
  font-size: 1.1rem;
  line-height: 1.7;
}

.adventure-content h2 {
  font-size: 1.8rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.adventure-content h3 {
  font-size: 1.5rem;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.adventure-content p {
  margin-bottom: 1.5rem;
}

.adventure-content ul, 
.adventure-content ol {
  margin-bottom: 1.5rem;
  padding-left: 1.5rem;
}

.adventure-content li {
  margin-bottom: 0.5rem;
}

.adventure-content img {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  margin: 1.5rem 0;
}

.prose {
  max-width: 65ch;
}
</style>
