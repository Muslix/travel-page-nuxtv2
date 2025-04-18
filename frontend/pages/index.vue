<template>
  <div>
    <!-- Hero-Banner mit aktuellem Abenteuer -->
    <div class="hero-banner">
      <v-carousel
        cycle
        height="650"
        hide-delimiter-background
        show-arrows="hover"
        interval="7000"
      >
        <v-carousel-item
          v-for="(featuredAdventure, i) in featuredAdventures"
          :key="i"
          :src="featuredAdventure.featured_image_url || 'https://images.unsplash.com/photo-1503220317375-aaad61436b1b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'"
          cover
        >
          <div class="hero-overlay d-flex flex-column justify-end">
            <v-container>
              <v-row>
                <v-col cols="12" md="8" lg="6">
                  <h3 class="text-overline text-white mb-1">Entdecke</h3>
                  <h1 class="text-h2 text-white font-weight-bold mb-3">{{ featuredAdventure.title }}</h1>
                  <p class="text-subtitle-1 text-white mb-4">{{ featuredAdventure.description }}</p>
                  <v-btn
                    color="accent"
                    size="large"
                    variant="elevated"
                    :to="`/abenteuer/${featuredAdventure.slug}`"
                    class="mb-8"
                  >
                    Abenteuer entdecken
                    <v-icon class="ml-2">mdi-arrow-right</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </div>
        </v-carousel-item>
      </v-carousel>
    </div>

    <!-- Aktuelle Abenteuer Sektion -->
    <v-container class="py-16">
      <v-row class="mb-8">
        <v-col cols="12" md="8">
          <h2 class="text-h3 font-weight-bold">Aktuelle Abenteuer</h2>
          <p class="text-subtitle-1">Entdecke meine neuesten Bikepacking-Touren und Radreisen</p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center">
          <v-btn
            color="primary"
            variant="text"
            to="/abenteuer"
            class="text-none"
          >
            Alle Abenteuer ansehen
            <v-icon class="ml-1">mdi-arrow-right</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      
      <div v-if="isLoading" class="d-flex justify-center my-12">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </div>
      
      <div v-else-if="error" class="text-center my-12">
        <v-alert type="error" title="Fehler beim Laden" :text="error.message"></v-alert>
        <v-btn color="primary" class="mt-6" @click="loadAdventures">Erneut versuchen</v-btn>
      </div>
      
      <div v-else-if="adventures.length === 0" class="text-center my-12">
        <v-alert type="info" title="Keine Abenteuer" text="Es wurden noch keine Abenteuer veröffentlicht."></v-alert>
      </div>
      
      <v-row v-else>
        <v-col v-for="adventure in adventures" :key="adventure.id" cols="12" sm="6" md="4">
          <v-hover v-slot="{ isHovering, props }">
            <v-card
              v-bind="props"
              :to="`/abenteuer/${adventure.slug}`"
              class="h-100 d-flex flex-column adventure-card"
              :elevation="isHovering ? 8 : 2"
              :class="{ 'on-hover': isHovering }"
            >
              <v-img
                :src="adventure.featured_image_url || 'https://images.unsplash.com/photo-1473861646675-0ca14fee6856?ixlib=rb-4.0.3&auto=format&fit=crop'"
                height="220"
                cover
                class="align-end"
              >
                <div class="adventure-image-gradient">
                  <div v-if="adventure.location" class="location-chip">
                    <v-icon size="small" class="mr-1">mdi-map-marker</v-icon>
                    {{ adventure.location }}
                  </div>
                </div>
              </v-img>
              
              <v-card-title class="text-h5">
                {{ adventure.title }}
              </v-card-title>
              
              <v-card-text class="flex-grow-1">
                <p class="adventure-description mb-4">{{ adventure.description }}</p>
                
                <div class="adventure-meta d-flex align-center">
                  <div v-if="adventure.duration_days" class="mr-4">
                    <v-icon size="small" color="primary" class="mr-1">mdi-calendar-range</v-icon>
                    {{ adventure.duration_days }} {{ adventure.duration_days === 1 ? 'Tag' : 'Tage' }}
                  </div>
                  <div v-if="adventure.distance_km" class="mr-4">
                    <v-icon size="small" color="primary" class="mr-1">mdi-map-marker-distance</v-icon>
                    {{ adventure.distance_km }} km
                  </div>
                  <div v-if="adventure.difficulty">
                    <v-icon size="small" color="primary" class="mr-1">mdi-terrain</v-icon>
                    {{ adventure.difficulty }}
                  </div>
                </div>
              </v-card-text>
              
              <v-divider></v-divider>
              
              <v-card-actions>
                <div v-if="adventure.tags && adventure.tags.length > 0" class="px-3">
                  <v-chip
                    v-for="tag in adventure.tags.slice(0, 2)"
                    :key="tag.id"
                    size="small"
                    color="primary"
                    variant="outlined"
                    class="mr-1"
                  >
                    {{ tag.name }}
                  </v-chip>
                  <span v-if="adventure.tags.length > 2" class="text-caption text-medium-emphasis ml-1">
                    +{{ adventure.tags.length - 2 }}
                  </span>
                </div>
                <v-spacer></v-spacer>
                <v-btn
                  variant="text"
                  color="primary"
                  class="font-weight-bold"
                >
                  Lesen
                  <v-icon size="small" class="ml-1">mdi-arrow-right</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-hover>
        </v-col>
      </v-row>
    </v-container>

    <!-- Kategorien mit Bildern -->
    <v-container fluid class="py-16 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" class="text-center">
            <h2 class="text-h3 font-weight-bold mb-3">Entdecke Bikepacking</h2>
            <p class="text-subtitle-1 mx-auto" style="max-width: 600px">
              Von Routen und Ausrüstung bis hin zu Tipps und Tricks - hier findest du alles für dein nächstes Abenteuer
            </p>
          </v-col>
        </v-row>
        
        <v-row>
          <v-col cols="12" md="4">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="{ 'on-hover': isHovering }"
                to="/routen"
                height="350"
                class="category-card"
              >
                <v-img
                  src="https://images.unsplash.com/photo-1534787238916-9ba6764efd4f?ixlib=rb-4.0.3&auto=format&fit=crop&w=3542&q=80"
                  height="350"
                  cover
                  class="category-image"
                >
                  <div class="d-flex flex-column justify-end fill-height pa-6">
                    <h3 class="text-h4 font-weight-bold text-white mb-2">Routen & Touren</h3>
                    <div class="bg-white category-divider mb-3"></div>
                    <p class="text-subtitle-1 text-white">Entdecke aufregende Bikepacking-Routen für dein nächstes Abenteuer</p>
                  </div>
                </v-img>
              </v-card>
            </v-hover>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="{ 'on-hover': isHovering }"
                to="/ausruestung"
                height="350"
                class="category-card"
              >
                <v-img
                  src="https://images.unsplash.com/photo-1475666675596-cca2035b3d79?ixlib=rb-4.0.3&auto=format&fit=crop&w=3540&q=80" 
                  height="350"
                  cover
                  class="category-image"
                >
                  <div class="d-flex flex-column justify-end fill-height pa-6">
                    <h3 class="text-h4 font-weight-bold text-white mb-2">Ausrüstung</h3>
                    <div class="bg-white category-divider mb-3"></div>
                    <p class="text-subtitle-1 text-white">Die besten Ausrüstungs-Tipps und Gear-Reviews für deine Tour</p>
                  </div>
                </v-img>
              </v-card>
            </v-hover>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="{ 'on-hover': isHovering }"
                to="/galerie"
                height="350"
                class="category-card"
              >
                <v-img
                  src="https://images.unsplash.com/photo-1539635278303-d4002c07eae3?ixlib=rb-4.0.3&auto=format&fit=crop&w=3540&q=80"
                  height="350"
                  cover
                  class="category-image"
                >
                  <div class="d-flex flex-column justify-end fill-height pa-6">
                    <h3 class="text-h4 font-weight-bold text-white mb-2">Galerie</h3>
                    <div class="bg-white category-divider mb-3"></div>
                    <p class="text-subtitle-1 text-white">Eindrucksvolle Bilder und Impressionen von unterwegs</p>
                  </div>
                </v-img>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
    </v-container>

    <!-- Über mich Sektion -->
    <v-container class="py-16">
      <v-row align="center">
        <v-col cols="12" md="5">
          <v-hover v-slot="{ isHovering, props }">
            <v-card
              v-bind="props"
              :elevation="isHovering ? 16 : 8"
              :class="{ 'on-hover': isHovering }"
              class="rounded-circle overflow-hidden mx-auto"
              style="width: 400px; height: 400px"
            >
              <v-img
                src="https://images.unsplash.com/photo-1561542320-9a18cd340469?ixlib=rb-4.0.3&auto=format&fit=crop&w=3000&q=80"
                height="100%"
                width="100%"
                cover
              ></v-img>
            </v-card>
          </v-hover>
        </v-col>
        <v-col cols="12" md="7">
          <h2 class="text-h3 font-weight-bold mb-4">Über Schwob aufm Sattl</h2>
          <p class="text-subtitle-1 mb-4">
            Hallo, ich bin Michael, ein begeisterter Radfahrer und Bikepacker aus dem schönen Schwaben. Auf diesem Blog teile ich meine Abenteuer, Routen und Ausrüstungstipps rund ums Radfahren und Bikepacking.
          </p>
          <p class="text-subtitle-1 mb-6">
            Von Tagesausflügen im Schwarzwald bis hin zu mehrwöchigen Touren durch die Alpen - hier findest du Inspiration und praktische Tipps für deine nächste Radreise.
          </p>
          <div class="d-flex align-center">
            <v-btn color="primary" to="/profil" size="large" class="mr-4">
              Mehr über mich
            </v-btn>
            <div class="social-icons">
              <v-btn icon="mdi-youtube" color="error" variant="text" href="https://youtube.com" target="_blank" class="mr-2"></v-btn>
              <v-btn icon="mdi-instagram" color="#E1306C" variant="text" href="https://instagram.com" target="_blank" class="mr-2"></v-btn>
              <v-btn icon="mdi-strava" color="#FC4C02" variant="text" href="https://strava.com" target="_blank"></v-btn>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>

    <!-- Newsletter Anmeldung -->
    <v-container fluid class="py-16 bg-primary">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" class="text-center mb-6">
            <h2 class="text-h3 font-weight-bold text-white mb-3">Newsletter abonnieren</h2>
            <p class="text-subtitle-1 text-white mb-0 mx-auto" style="max-width: 600px">
              Erhalte Updates zu neuen Touren, Ausrüstungstipps und exklusive Inhalte
            </p>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-form @submit.prevent="subscribeToNewsletter">
              <v-row>
                <v-col cols="12" sm="8">
                  <v-text-field
                    v-model="newsletter.email"
                    label="Deine E-Mail-Adresse"
                    variant="outlined"
                    bg-color="white"
                    density="comfortable"
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-btn 
                    type="submit" 
                    color="accent" 
                    block
                    :loading="newsletter.loading"
                    size="large"
                  >
                    Abonnieren
                  </v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-col>
        </v-row>
      </v-container>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useHead } from 'nuxt/app'
import type { Adventure } from '@/types/adventure'
import adventureService from '@/services/adventure-service'

// State für Abenteuer
const adventures = ref<Adventure[]>([])
const isLoading = ref(true)
const error = ref<Error | null>(null)

// State für Newsletter
const newsletter = ref({ email: '', loading: false, success: false, error: null as string | null })

// Featured Abenteuer für Hero
const featuredAdventures = computed(() => {
  return adventures.value.length > 0
    ? adventures.value.slice(0, 3)
    : [
        {
          id: '0',
          title: 'Bikepacking Abenteuer',
          slug: '#',
          description: 'Entdecke spannende Bikepacking-Routen und Abenteuer auf zwei Rädern',
          featured_image_url: 'https://images.unsplash.com/photo-1503220317375-aaad61436b1b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        }
      ]
})

// Abenteuer laden
async function loadAdventures() {
  isLoading.value = true
  error.value = null
  try {
    const { adventures: items, error: err } = await adventureService.getAdventures({ status: 'published', limit: 6 })
    if (err) throw err
    adventures.value = items
  } catch (e) {
    error.value = e as Error
  } finally {
    isLoading.value = false
  }
}

// Newsletter Anmeldung
async function subscribeToNewsletter() {
  if (!newsletter.value.email) return
  newsletter.value.loading = true
  newsletter.value.error = null
  try {
    // TODO: Implement API call
    newsletter.value.success = true
    alert(`Danke für deine Anmeldung, ${newsletter.value.email}!`)
    newsletter.value.email = ''
  } catch (e) {
    newsletter.value.error = 'Fehler bei der Anmeldung.'
  } finally {
    newsletter.value.loading = false
  }
}

// Lifecycle & Meta
onMounted(loadAdventures)
useHead({ title: 'Schwob aufm Sattl - Startseite' })
</script>

<style>
.adventure-description {
  -webkit-line-clamp: 3;
  line-clamp: 3;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.on-hover {
  transition: all 0.3s ease-in-out;
  transform: translateY(-5px);
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.4) 40%, rgba(0,0,0,0) 100%);
  padding-top: 150px;
}

.category-card {
  overflow: hidden;
  transition: all 0.3s ease;
}

.category-image::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.2) 60%, rgba(0,0,0,0) 100%);
}

.category-divider {
  width: 60px;
  height: 4px;
  border-radius: 2px;
}

.adventure-image-gradient {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 100%);
  padding: 16px;
}

.location-chip {
  color: white;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
}

.adventure-meta {
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
}

@media (max-width: 600px) {
  .hero-overlay {
    padding-top: 80px;
  }
}
</style>
