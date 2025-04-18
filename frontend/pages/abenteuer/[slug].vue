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
              <div v-html="renderMarkdown(adventure.content)" class="prose max-w-none"></div>
            </div>
            
            <!-- Galerie-Abschnitt -->
            <div v-if="adventure.images && adventure.images.length > 0" class="mt-12">
              <h2 class="text-h4 mb-4">Impressionen</h2>
              <v-row>
                <v-col v-for="(image, index) in adventure.images" :key="index" cols="12" sm="6" md="4">
                  <v-img
                    :src="image.url"
                    :alt="image.alt || `Bild ${index + 1} von ${adventure.title}`"
                    aspect-ratio="1"
                    class="rounded-lg elevation-2"
                    cover
                    @click="openGallery(index)"
                  ></v-img>
                </v-col>
              </v-row>
            </div>
          </v-col>

          <v-col cols="12" md="4">
            <!-- Info-Box -->
            <v-card class="mb-6">
              <v-card-title class="bg-primary text-white">
                Tour auf einen Blick
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item v-if="adventure.location">
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-map-marker</v-icon>
                    </template>
                    <v-list-item-title>{{ adventure.location }}</v-list-item-title>
                    <v-list-item-subtitle>Ort</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item v-if="adventure.distance_km">
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-map-marker-distance</v-icon>
                    </template>
                    <v-list-item-title>{{ adventure.distance_km }} km</v-list-item-title>
                    <v-list-item-subtitle>Distanz</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item v-if="adventure.elevation_m">
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-slope-uphill</v-icon>
                    </template>
                    <v-list-item-title>{{ adventure.elevation_m }} m</v-list-item-title>
                    <v-list-item-subtitle>Höhenmeter</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item v-if="adventure.duration_days">
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-calendar-range</v-icon>
                    </template>
                    <v-list-item-title>{{ adventure.duration_days }} {{ adventure.duration_days === 1 ? 'Tag' : 'Tage' }}</v-list-item-title>
                    <v-list-item-subtitle>Dauer</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item v-if="adventure.difficulty">
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-arm-flex</v-icon>
                    </template>
                    <v-list-item-title>{{ adventure.difficulty }}</v-list-item-title>
                    <v-list-item-subtitle>Schwierigkeitsgrad</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <!-- Autor-Box -->
            <v-card v-if="adventure.profile" class="mb-6">
              <v-card-title class="bg-primary text-white">
                Autor
              </v-card-title>
              <v-card-text class="pt-4">
                <div class="d-flex align-center">
                  <v-avatar size="64" class="mr-4">
                    <v-img :src="adventure.profile.avatar_url || 'https://cdn.vuetifyjs.com/images/john.jpg'" />
                  </v-avatar>
                  <div>
                    <div class="text-h6">{{ adventure.profile.name }}</div>
                    <v-btn
                      variant="text"
                      color="primary"
                      :to="`/profil/${adventure.profile.slug}`"
                      class="px-0"
                    >
                      Profil anzeigen
                    </v-btn>
                  </div>
                </div>
              </v-card-text>
            </v-card>

            <!-- Teilen -->
            <v-card>
              <v-card-title class="bg-primary text-white">
                Teilen
              </v-card-title>
              <v-card-text>
                <div class="d-flex justify-space-around py-2">
                  <v-btn icon color="#1877F2" @click="shareOnFacebook">
                    <v-icon>mdi-facebook</v-icon>
                  </v-btn>
                  <v-btn icon color="#1DA1F2" @click="shareOnTwitter">
                    <v-icon>mdi-twitter</v-icon>
                  </v-btn>
                  <v-btn icon color="#25D366" @click="shareOnWhatsApp">
                    <v-icon>mdi-whatsapp</v-icon>
                  </v-btn>
                  <v-btn icon color="#2867B2" @click="shareOnLinkedIn">
                    <v-icon>mdi-linkedin</v-icon>
                  </v-btn>
                  <v-btn icon @click="copyLink">
                    <v-icon>mdi-link-variant</v-icon>
                  </v-btn>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <!-- Bildergalerie-Dialog -->
      <v-dialog v-model="galleryDialog" fullscreen>
        <v-card>
          <v-toolbar dark color="primary">
            <v-btn icon dark @click="galleryDialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>Galerie: {{ adventure.title }}</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon dark @click="currentImageIndex = Math.max(0, currentImageIndex - 1)">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <v-btn icon dark @click="currentImageIndex = Math.min(adventure.images.length - 1, currentImageIndex + 1)">
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-toolbar>
          <div class="d-flex justify-center align-center" style="height: calc(100vh - 64px)">
            <v-img
              v-if="adventure.images && adventure.images.length > 0"
              :src="adventure.images[currentImageIndex].url"
              :alt="adventure.images[currentImageIndex].alt"
              max-height="90vh"
              max-width="90vw"
              contain
            ></v-img>
          </div>
        </v-card>
      </v-dialog>

      <!-- Ähnliche Abenteuer -->
      <v-container class="py-8">
        <h2 class="text-h4 mb-6">Ähnliche Abenteuer</h2>
        <adventure-cards :limit="3" :exclude-id="adventure.id" :tags="adventure.tags?.map(tag => tag.slug)" />
      </v-container>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { marked } from 'marked';
import type { Adventure } from '~/types/adventure';
import adventureService from '~/services/adventure-service';

const route = useRoute();
const adventure = ref<Adventure | null>(null);
const isLoading = ref(true);
const error = ref<Error | null>(null);
const galleryDialog = ref(false);
const currentImageIndex = ref(0);

// Slug aus der URL holen
const slug = computed(() => route.params.slug as string);

// Adventure laden
async function loadAdventure() {
  isLoading.value = true;
  error.value = null;
  
  try {
    adventure.value = await adventureService.getAdventureBySlug(slug.value);
  } catch (err) {
    error.value = err as Error;
    console.error('Fehler beim Laden des Abenteuers:', err);
  } finally {
    isLoading.value = false;
  }
}

// Markdown zu HTML rendern
function renderMarkdown(content: string): string {
  if (!content) return '';
  return marked(content);
}

// Galerie öffnen
function openGallery(index: number) {
  currentImageIndex.value = index;
  galleryDialog.value = true;
}

// Social Media Sharing
function shareOnFacebook() {
  const url = encodeURIComponent(window.location.href);
  const title = encodeURIComponent(adventure.value?.title || '');
  window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}&t=${title}`, '_blank');
}

function shareOnTwitter() {
  const url = encodeURIComponent(window.location.href);
  const text = encodeURIComponent(`${adventure.value?.title || ''}`);
  window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank');
}

function shareOnWhatsApp() {
  const url = encodeURIComponent(window.location.href);
  const text = encodeURIComponent(`${adventure.value?.title || ''}: ${window.location.href}`);
  window.open(`https://wa.me/?text=${text}`, '_blank');
}

function shareOnLinkedIn() {
  const url = encodeURIComponent(window.location.href);
  const title = encodeURIComponent(adventure.value?.title || '');
  window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank');
}

function copyLink() {
  navigator.clipboard.writeText(window.location.href);
  // Hier könnte eine Benachrichtigung angezeigt werden
}

// Beim Mounten der Komponente das Abenteuer laden
onMounted(() => {
  loadAdventure();
});

// Titel für die Seite setzen
useHead(() => ({
  title: adventure.value ? `${adventure.value.title} | Schwob aufm Sattl` : 'Abenteuer | Schwob aufm Sattl',
  meta: [
    {
      name: 'description',
      content: adventure.value?.description || 'Bikepacking und Radabenteuer'
    }
  ]
}));
</script>

<style scoped>
.adventure-hero {
  position: relative;
}

.adventure-content {
  font-size: 1.125rem;
  line-height: 1.75;
}

.adventure-content :deep(h1),
.adventure-content :deep(h2),
.adventure-content :deep(h3),
.adventure-content :deep(h4),
.adventure-content :deep(h5),
.adventure-content :deep(h6) {
  margin-top: 1.5em;
  margin-bottom: 0.75em;
  font-weight: 600;
  line-height: 1.25;
}

.adventure-content :deep(h1) {
  font-size: 2.25rem;
}

.adventure-content :deep(h2) {
  font-size: 1.875rem;
}

.adventure-content :deep(h3) {
  font-size: 1.5rem;
}

.adventure-content :deep(p) {
  margin-bottom: 1.25rem;
}

.adventure-content :deep(ul),
.adventure-content :deep(ol) {
  margin-bottom: 1.25rem;
  padding-left: 1.5rem;
}

.adventure-content :deep(li) {
  margin-bottom: 0.5rem;
}

.adventure-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  margin: 1.5rem 0;
}

.adventure-content :deep(blockquote) {
  border-left: 4px solid #ccc;
  padding-left: 1rem;
  font-style: italic;
  margin: 1.5rem 0;
}

.adventure-content :deep(pre) {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin: 1.5rem 0;
}

.adventure-content :deep(code) {
  font-family: monospace;
  background-color: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
}
</style>
