<template>
  <div>
    <!-- Hero-Banner mit aktuellem Abenteuer -->
    <v-parallax
      src="https://images.unsplash.com/photo-1503220317375-aaad61436b1b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"
      height="500"
    >
      <div class="d-flex flex-column fill-height justify-center align-center text-white">
        <h1 class="text-h2 font-weight-bold mb-4">Schwob aufm Sattl</h1>
        <h2 class="text-h4 mb-6">Bikepacking & Radreise Abenteuer</h2>
        <v-btn
          color="accent"
          size="large"
          variant="elevated"
          to="/abenteuer/aktuell"
        >
          Aktuelles Abenteuer erkunden
        </v-btn>
      </div>
    </v-parallax>

    <!-- Aktuelle Abenteuer Sektion -->
    <v-container class="py-12">
      <h2 class="text-h4 mb-6 text-center">Aktuelle Abenteuer</h2>
      
      <div v-if="isLoading" class="d-flex justify-center my-6">
        <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
      </div>
      
      <div v-else-if="error" class="text-center my-6">
        <v-alert type="error" title="Fehler beim Laden" :text="error.message"></v-alert>
        <v-btn color="primary" class="mt-4" @click="loadAdventures">Erneut versuchen</v-btn>
      </div>
      
      <div v-else-if="adventures.length === 0" class="text-center my-6">
        <v-alert type="info" title="Keine Abenteuer" text="Es wurden noch keine Abenteuer veröffentlicht."></v-alert>
      </div>
      
      <v-row v-else>
        <v-col cols="12" md="4" v-for="adventure in adventures" :key="adventure.id">
          <v-card class="h-100 d-flex flex-column" :to="`/abenteuer/${adventure.slug}`">
            <v-img
              :src="adventure.featured_image_url || 'https://images.unsplash.com/photo-1473861646675-0ca14fee6856?ixlib=rb-4.0.3&auto=format&fit=crop'"
              height="200"
              cover
            ></v-img>
            <v-card-title>{{ adventure.title }}</v-card-title>
            <v-card-subtitle v-if="adventure.tags && adventure.tags.length > 0" class="pb-0">
              <v-chip-group>
                <v-chip v-for="tag in adventure.tags.slice(0, 3)" :key="tag.id" size="small" color="primary" variant="outlined">
                  {{ tag.name }}
                </v-chip>
              </v-chip-group>
            </v-card-subtitle>
            <v-card-text class="flex-grow-1">
              {{ adventure.description }}
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" variant="text">Mehr erfahren</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Ausrüstungs-Highlights -->
    <v-container class="py-10 bg-grey-lighten-4">
      <h2 class="text-h4 mb-6 text-center">Ausrüstungs-Highlights</h2>
      
      <v-row>
        <v-col cols="12" md="6" lg="3" v-for="n in 4" :key="n">
          <v-card variant="outlined">
            <v-card-title>Ausrüstungsteil {{ n }}</v-card-title>
            <v-card-text>
              Die wichtigsten Ausrüstungsteile für dein nächstes Abenteuer.
            </v-card-text>
            <v-card-actions>
              <v-btn color="secondary" variant="text" to="/ausruestung">Details</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Newsletter Anmeldung -->
    <v-container class="py-12 text-center">
      <h2 class="text-h4 mb-3">Bleib auf dem Laufenden</h2>
      <p class="mb-6">Abonniere den Newsletter, um keine Abenteuer zu verpassen.</p>
      
      <v-row justify="center">
        <v-col cols="12" md="6">
          <v-form>
            <v-text-field
              label="E-Mail Adresse"
              variant="outlined"
              append-inner-icon="mdi-email-outline"
            ></v-text-field>
            <v-btn color="primary" size="large" block>Abonnieren</v-btn>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import useAdventureService from '~/services/adventure-service';
import type { Adventure } from '~/types/adventure';

// Adventure-Daten
const adventures = ref<Adventure[]>([]);
const isLoading = ref(true);
const error = ref<Error | null>(null);

const adventureService = useAdventureService();

async function loadAdventures() {
  isLoading.value = true;
  error.value = null;
  
  try {
    const { adventures: loadedAdventures, error: loadError } = await adventureService.getAllAdventures();
    
    if (loadError) {
      error.value = loadError as Error;
    } else {
      adventures.value = loadedAdventures || [];
    }
  } catch (err) {
    console.error('Failed to load adventures:', err);
    error.value = err as Error;
  } finally {
    isLoading.value = false;
  }
}

onMounted(async () => {
  await loadAdventures();
});
</script>

<style scoped>
/* Page specific styles */
</style>
