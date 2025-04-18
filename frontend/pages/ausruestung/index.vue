<template>
  <div>
    <!-- Hero-Banner für die Ausrüstungsseite -->
    <div class="equipment-hero relative">
      <v-img
        src="https://images.unsplash.com/photo-1504025468847-0e438279542c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3540&q=80"
        height="400"
        cover
      >
        <div class="absolute inset-0 bg-gradient-to-b from-black/50 to-black/70 flex items-center">
          <v-container>
            <h1 class="text-h2 font-weight-bold text-white mb-4">Ausrüstung</h1>
            <p class="text-h6 text-white max-w-lg">Empfehlungen, Tests und Erfahrungsberichte zu Bikepacking- und Outdoor-Ausrüstung</p>
          </v-container>
        </div>
      </v-img>
    </div>

    <v-container class="py-12">
      <!-- Kategorie-Filter -->
      <v-row class="mb-8">
        <v-col cols="12" md="8">
          <h2 class="text-h4 font-weight-bold mb-2">Meine Ausrüstungsempfehlungen</h2>
          <p class="text-subtitle-1">Ausrüstung, die ich auf meinen Touren verwende und empfehlen kann</p>
        </v-col>
        <v-col cols="12" md="4">
          <v-select
            v-model="selectedCategory"
            :items="['Alle Kategorien', ...categories.map(cat => cat.name)]"
            label="Kategorie filtern"
            variant="outlined"
            hide-details
            density="comfortable"
            @update:model-value="filterEquipment"
          ></v-select>
        </v-col>
      </v-row>

      <!-- Loading, Error und Empty States -->
      <div v-if="isLoading" class="d-flex justify-center my-12">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </div>
      
      <div v-else-if="error" class="text-center my-12">
        <v-alert type="error" title="Fehler beim Laden" :text="error.message"></v-alert>
        <v-btn color="primary" class="mt-6" @click="loadEquipment">Erneut versuchen</v-btn>
      </div>
      
      <div v-else-if="filteredEquipment.length === 0" class="text-center my-12">
        <v-alert type="info" title="Keine Ausrüstung" text="Für diese Kategorie wurden noch keine Ausrüstungsgegenstände hinzugefügt."></v-alert>
      </div>
      
      <!-- Equipment List -->
      <v-row v-else>
        <v-col v-for="(item, index) in filteredEquipment" :key="item.id" cols="12">
          <v-hover v-slot="{ isHovering, props }">
            <v-card
              v-bind="props"
              :elevation="isHovering ? 8 : 2"
              :class="{ 'on-hover': isHovering }"
              class="equipment-card mb-6"
            >
              <v-row no-gutters>
                <v-col cols="12" md="4">
                  <v-img
                    :src="item.image_url || `https://source.unsplash.com/random/600x400?${encodeURIComponent(item.name)}`"
                    height="100%"
                    cover
                    class="h-100"
                    :class="{'darken-image-in-dark-mode': isDarkMode}"
                  >
                    <div class="equipment-category-badge">
                      {{ getCategoryName(item.category_id) }}
                    </div>
                  </v-img>
                </v-col>
                <v-col cols="12" md="8">
                  <v-card-item>
                    <v-card-title class="text-h4 mb-2">{{ item.name }}</v-card-title>
                    <v-card-subtitle class="mb-3">
                      <div class="d-flex align-center">
                        <v-rating
                          v-if="item.rating"
                          :model-value="item.rating"
                          color="amber"
                          density="compact"
                          half-increments
                          readonly
                          size="small"
                          class="mr-2"
                        ></v-rating>
                        <span v-if="item.rating" class="text-medium-emphasis">{{ item.rating }} / 5</span>
                      </div>
                    </v-card-subtitle>
                  </v-card-item>
                  
                  <v-card-text>
                    <p class="text-body-1 mb-4">{{ item.description }}</p>
                    
                    <div class="equipment-specs d-flex flex-wrap">
                      <v-chip v-if="item.price" class="mr-2 mb-2" color="primary" variant="outlined">
                        <v-icon start size="small">mdi-currency-eur</v-icon>
                        {{ formatPrice(item.price) }}
                      </v-chip>
                      
                      <v-chip v-if="item.weight_grams" class="mr-2 mb-2" color="primary" variant="outlined">
                        <v-icon start size="small">mdi-weight</v-icon>
                        {{ formatWeight(item.weight_grams) }}
                      </v-chip>
                      
                      <v-chip v-if="item.purchase_date" class="mr-2 mb-2" color="primary" variant="outlined">
                        <v-icon start size="small">mdi-calendar</v-icon>
                        {{ formatDate(item.purchase_date) }}
                      </v-chip>
                    </div>
                  </v-card-text>
                  
                  <v-card-actions>
                    <v-btn
                      color="primary"
                      variant="text"
                      @click="expandedItems[index] = !expandedItems[index]"
                    >
                      {{ expandedItems[index] ? 'Weniger anzeigen' : 'Mehr erfahren' }}
                      <v-icon right>
                        {{ expandedItems[index] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                      </v-icon>
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                      v-if="item.affiliate_link"
                      color="accent"
                      variant="elevated"
                      :href="item.affiliate_link"
                      target="_blank"
                    >
                      Kaufen
                      <v-icon right>mdi-open-in-new</v-icon>
                    </v-btn>
                  </v-card-actions>
                  
                  <v-expand-transition>
                    <div v-if="expandedItems[index]">
                      <v-divider></v-divider>
                      <v-card-text>
                        <div v-if="item.details" class="equipment-details">
                          <div v-html="renderMarkdown(item.details)"></div>
                        </div>
                        <div v-else class="text-center text-body-2 text-medium-emphasis py-8">
                          Detaillierte Beschreibung folgt in Kürze...
                        </div>
                      </v-card-text>
                    </div>
                  </v-expand-transition>
                </v-col>
              </v-row>
            </v-card>
          </v-hover>
        </v-col>
      </v-row>
    </v-container>
    
    <!-- Beliebteste Kategorien -->
    <v-container fluid class="py-12 bg-grey-lighten-4">
      <v-container>
        <h2 class="text-h4 font-weight-bold mb-8 text-center">Beliebteste Kategorien</h2>
        
        <v-row>
          <v-col v-for="category in topCategories" :key="category.id" cols="12" sm="6" md="3">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="{ 'on-hover': isHovering }"
                class="category-card"
                height="200"
                @click="selectCategory(category.name)"
              >
                <v-img
                  :src="getCategoryImage(category.slug)"
                  height="200"
                  cover
                  class="category-image"
                >
                  <div class="d-flex flex-column justify-center align-center fill-height">
                    <h3 class="text-h5 font-weight-bold text-white text-center">{{ category.name }}</h3>
                    <div class="text-subtitle-2 text-white text-center mt-2">
                      {{ getItemCountByCategory(category.id) }} Artikel
                    </div>
                  </div>
                </v-img>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
    </v-container>
    
    <!-- Tipps zum Packen -->
    <v-container class="py-12">
      <v-row>
        <v-col cols="12" md="6">
          <h2 class="text-h4 font-weight-bold mb-4">Packtipps für Bikepacking</h2>
          <p class="text-subtitle-1 mb-4">
            Die richtige Ausrüstung ist nur der halbe Weg zum Erfolg - sie muss auch richtig gepackt werden.
          </p>
          <p class="text-body-1 mb-4">
            Beim Bikepacking geht es darum, das Gewicht gleichmäßig zu verteilen und den Schwerpunkt niedrig zu halten.
            Hier sind meine wichtigsten Tipps für effizientes Packen:
          </p>
          <v-list class="bg-transparent">
            <v-list-item prepend-icon="mdi-chevron-right" class="mb-2">
              <v-list-item-title>Schweres Gepäck (Kocher, Werkzeug) möglichst tief und nah am Rahmen packen</v-list-item-title>
            </v-list-item>
            <v-list-item prepend-icon="mdi-chevron-right" class="mb-2">
              <v-list-item-title>Oft benötigte Dinge (Snacks, Kamera) in leicht zugänglichen Taschen verstauen</v-list-item-title>
            </v-list-item>
            <v-list-item prepend-icon="mdi-chevron-right" class="mb-2">
              <v-list-item-title>Nach Funktionen und nicht nach Gegenständen packen (z.B. "Kochen" statt "Kocher, Besteck, Tasse, etc.")</v-list-item-title>
            </v-list-item>
            <v-list-item prepend-icon="mdi-chevron-right">
              <v-list-item-title>Wasserdichte Packsäcke für Elektronik und Kleidung verwenden</v-list-item-title>
            </v-list-item>
          </v-list>
          <v-btn
            color="primary"
            class="mt-4"
            variant="outlined"
            href="/blog/ultraleichtes-packen-bikepacking"
          >
            Kompletten Packtipp-Artikel lesen
          </v-btn>
        </v-col>
        <v-col cols="12" md="6">
          <v-img
            src="https://images.unsplash.com/photo-1559521783-1d1f4815a1c5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2066&q=80"
            alt="Bikepacking Ausrüstung"
            class="rounded-lg elevation-3"
            height="450"
            cover
          ></v-img>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useTheme } from 'vuetify';
import { marked } from 'marked';

// Types
interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
}

interface Equipment {
  id: number;
  name: string;
  slug: string;
  description: string;
  details: string | null;
  rating: number | null;
  price: number | null;
  purchase_date: string | null;
  weight_grams: number | null;
  category_id: number;
  image_url?: string;
  affiliate_link?: string;
}

// Statemanagement
const theme = useTheme();
const isDarkMode = computed(() => theme.global.current.value.dark);
const equipment = ref<Equipment[]>([]);
const categories = ref<Category[]>([]);
const isLoading = ref(true);
const error = ref<Error | null>(null);
const selectedCategory = ref('Alle Kategorien');
const expandedItems = ref<Record<number, boolean>>({});

// Berechnete Eigenschaften
const filteredEquipment = computed(() => {
  if (selectedCategory.value === 'Alle Kategorien') {
    return equipment.value;
  } else {
    const category = categories.value.find(cat => cat.name === selectedCategory.value);
    return category 
      ? equipment.value.filter(item => item.category_id === category.id)
      : equipment.value;
  }
});

const topCategories = computed(() => {
  // Die 4 Kategorien mit den meisten Ausrüstungsgegenständen
  const catCounts = categories.value.map(cat => ({
    ...cat,
    count: equipment.value.filter(item => item.category_id === cat.id).length
  }));
  
  return catCounts.sort((a, b) => b.count - a.count).slice(0, 4);
});

// Methoden
function getCategoryName(categoryId: number): string {
  const category = categories.value.find(cat => cat.id === categoryId);
  return category ? category.name : '';
}

function getCategoryImage(categorySlug: string): string {
  const categoryImages: Record<string, string> = {
    'fahrrad': 'https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?ixlib=rb-4.0.3&auto=format&fit=crop&w=3540&q=80',
    'bikepacking-taschen': 'https://images.unsplash.com/photo-1616684444017-dca482751c17?ixlib=rb-4.0.3&auto=format&fit=crop&w=2080&q=80',
    'camping': 'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?ixlib=rb-4.0.3&auto=format&fit=crop&w=3474&q=80',
    'bekleidung': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?ixlib=rb-4.0.3&auto=format&fit=crop&w=3474&q=80',
    'navigation': 'https://images.unsplash.com/photo-1452421822248-d4c2b47f0c81?ixlib=rb-4.0.3&auto=format&fit=crop&w=3474&q=80',
    'werkzeug': 'https://images.unsplash.com/photo-1581166397057-235af2b3c6dd?ixlib=rb-4.0.3&auto=format&fit=crop&w=3540&q=80',
    'elektronik': 'https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=3540&q=80',
    'packsaecke': 'https://images.unsplash.com/photo-1599751449318-df8c0c9a580d?ixlib=rb-4.0.3&auto=format&fit=crop&w=3444&q=80',
  };
  
  return categoryImages[categorySlug] || 'https://images.unsplash.com/photo-1504025468847-0e438279542c?ixlib=rb-4.0.3&auto=format&fit=crop&w=3540&q=80';
}

function getItemCountByCategory(categoryId: number): number {
  return equipment.value.filter(item => item.category_id === categoryId).length;
}

function selectCategory(categoryName: string): void {
  selectedCategory.value = categoryName;
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

function filterEquipment(): void {
  // Nichts zu tun da filteredEquipment bereits ein computed ist
}

function formatPrice(price: number): string {
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(price);
}

function formatWeight(weightGrams: number): string {
  return weightGrams >= 1000 
    ? `${(weightGrams / 1000).toFixed(2)} kg`
    : `${weightGrams} g`;
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('de-DE', { year: 'numeric', month: 'long' });
}

function renderMarkdown(markdown: string): string {
  return marked(markdown || '');
}

async function loadEquipment() {
  isLoading.value = true;
  error.value = null;
  
  try {
    // Mock-Daten laden (später durch API-Aufruf ersetzen)
    await loadMockData();
  } catch (err) {
    error.value = err as Error;
    console.error('Fehler beim Laden der Ausrüstung:', err);
  } finally {
    isLoading.value = false;
  }
}

// Mock-Daten für die Entwicklung
async function loadMockData() {
  // Simulation einer API-Latenz
  await new Promise(resolve => setTimeout(resolve, 800));
  
  categories.value = [
    { id: 1, name: 'Fahrrad', slug: 'fahrrad', description: 'Verschiedene Fahrradtypen und Rahmen' },
    { id: 2, name: 'Bikepacking-Taschen', slug: 'bikepacking-taschen', description: 'Taschen für Bikepacking-Touren' },
    { id: 3, name: 'Camping', slug: 'camping', description: 'Camping-Ausrüstung wie Zelte, Schlafsäcke, Kocher etc.' },
    { id: 4, name: 'Bekleidung', slug: 'bekleidung', description: 'Funktionskleidung für Radreisen' },
    { id: 5, name: 'Navigation', slug: 'navigation', description: 'GPS-Geräte, Smartphone-Halterungen und Apps' },
    { id: 6, name: 'Werkzeug', slug: 'werkzeug', description: 'Werkzeug und Reparatur-Sets für unterwegs' },
    { id: 7, name: 'Elektronik', slug: 'elektronik', description: 'Kameras, Powerbanks, Ladegeräte etc.' },
    { id: 8, name: 'Packsäcke', slug: 'packsaecke', description: 'Wasserdichte Packsäcke und Organisationshilfen' }
  ];
  
  equipment.value = [
    {
      id: 1,
      name: 'Specialized Diverge',
      slug: 'specialized-diverge',
      description: 'Mein Gravelbike für Bikepacking-Touren mit hervorragender Balance zwischen Komfort und Geschwindigkeit.',
      details: `# Specialized Diverge
Ein vielseitiges Gravelbike, das sich perfekt für längere Bikepacking-Touren eignet.

## Technische Daten
- Rahmen: Specialized Diverge Carbon
- Schaltung: Shimano GRX 2x11
- Bremsen: Hydraulische Scheibenbremsen
- Laufräder: DT Swiss G1800
- Reifen: WTB Riddler 45c tubeless

## Erfahrungen
Hat mich bisher auf allen Abenteuern zuverlässig begleitet und ist sowohl auf Asphalt als auch auf Schotter eine wahre Freude.`,
      rating: 5,
      price: 2800.00,
      purchase_date: '2022-03-15',
      weight_grams: 9200,
      category_id: 1,
      image_url: 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?ixlib=rb-4.0.3&auto=format&fit=crop&w=3540&q=80',
      affiliate_link: 'https://www.specialized.com/de/de/diverge'
    },
    {
      id: 2,
      name: 'Ortlieb Seat-Pack',
      slug: 'ortlieb-seat-pack',
      description: 'Wasserdichte Satteltasche mit 16,5 Liter Volumen - absolut zuverlässig auch bei schlechtem Wetter.',
      details: `# Ortlieb Seat-Pack
Eine robuste, wasserdichte Satteltasche für Bikepacking-Abenteuer.

## Spezifikationen
- Volumen: 16,5 Liter
- Gewicht: 456g
- Material: PU-beschichtetes Nylon
- Wasserdicht (IP64)

## Vorteile
- Absolut wasserdicht
- Stabil auch bei holprigen Abfahrten
- Einfache Montage
- Gutes Packvolumen

## Nachteile
- Etwas schwerer als manche Alternativen
- Keine externen Taschen für Kleinteile`,
      rating: 5,
      price: 135.00,
      purchase_date: '2022-04-10',
      weight_grams: 456,
      category_id: 2,
      image_url: 'https://images.unsplash.com/photo-1596894783047-507970c6c58e?ixlib=rb-4.0.3&auto=format&fit=crop&w=3540&q=80',
      affiliate_link: 'https://www.ortlieb.com/de_de/seat-pack'
    },
    {
      id: 3,
      name: 'MSR Hubba Hubba NX2',
      slug: 'msr-hubba-hubba-nx2',
      description: 'Leichtes 2-Personen-Zelt für Bikepacking und Trekking mit optimalem Gewicht-Komfort-Verhältnis.',
      details: `# MSR Hubba Hubba NX2
Ein ultraleichtes 2-Personen-Zelt, das sich hervorragend für Bikepacking eignet.

## Technische Daten
- Gewicht: 1,72 kg
- Packmaß: 46 x 15 cm
- Innenfläche: 2,7 m²
- 2 Eingänge und 2 Apsiden

## Erfahrungen
Das Zelt bietet ein ausgezeichnetes Verhältnis von Gewicht zu Komfort. Es ist schnell aufgebaut, bietet guten Wetterschutz und ist dabei kompakt genug, um es problemlos am Fahrrad zu transportieren.`,
      rating: 4,
      price: 430.00,
      purchase_date: '2022-05-03',
      weight_grams: 1720,
      category_id: 3,
      image_url: 'https://images.unsplash.com/photo-1536434750005-06336fdf6908?ixlib=rb-4.0.3&auto=format&fit=crop&w=4360&q=80',
      affiliate_link: 'https://www.msrgear.com/tents/backpacking-tents/hubba-hubba-nx-2-person-backpacking-tent'
    },
    {
      id: 4,
      name: 'Topeak Mini 20 Pro',
      slug: 'topeak-mini-20-pro',
      description: 'Kompaktes Multi-Tool mit 20 Funktionen - der perfekte Begleiter für Reparaturen unterwegs.',
      details: `# Topeak Mini 20 Pro
Ein vielseitiges Multi-Tool für unterwegs.

## Funktionen
- Verschiedene Inbus-Schlüssel (2-8mm)
- Torx T10, T15, T25
- Kreuz- und Schlitzschraubendreher
- Kettennieter
- Reifenheber
- Speichenschlüssel

## Vorteile
- Robust und langlebig
- Kompakte Größe
- Umfassende Werkzeugausstattung
- Praktische Tasche inklusive`,
      rating: 5,
      price: 39.99,
      purchase_date: '2022-03-20',
      weight_grams: 163,
      category_id: 6,
      image_url: 'https://images.unsplash.com/photo-1562280963-8a5475740a10?ixlib=rb-4.0.3&auto=format&fit=crop&w=2874&q=80',
      affiliate_link: 'https://www.topeak.com/global/de/product/269-MINI-20-PRO'
    },
    {
      id: 5,
      name: 'Garmin eTrex 32x',
      slug: 'garmin-etrex-32x',
      description: 'Robustes GPS-Gerät für Navigation im Gelände - unabhängig vom Smartphone-Akku.',
      details: `# Garmin eTrex 32x
Ein zuverlässiger GPS-Begleiter für alle Outdoor-Abenteuer.

## Technische Daten
- 2,2" Farbdisplay
- 8 GB interner Speicher
- Bis zu 25 Stunden Akkulaufzeit (2 AA-Batterien)
- Barometrischer Höhenmesser und 3-Achsen-Kompass
- Wasserdicht nach IPX7

## Erfahrungen
Vor allem in Regionen mit schlechtem Handyempfang ist das eTrex ein unverzichtbarer Begleiter. Die Kartendarstellung ist klar und präzise, die Batterielaufzeit beeindruckend.`,
      rating: 4,
      price: 249.99,
      purchase_date: '2021-11-15',
      weight_grams: 142,
      category_id: 5,
      image_url: 'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=3474&q=80',
      affiliate_link: 'https://www.garmin.com/de-DE/p/621225'
    }
  ];
}

// Beim Mounten der Komponente die Ausrüstung laden
onMounted(() => {
  loadEquipment();
});

// Titel für die Seite setzen
useHead({
  title: 'Ausrüstung | Schwob aufm Sattl',
  meta: [
    { 
      name: 'description',
      content: 'Bikepacking- und Radreise-Ausrüstung: Empfehlungen, Tests und Erfahrungsberichte zu Fahrrädern, Taschen, Zelten und mehr.'
    }
  ]
});
</script>

<style scoped>
.equipment-card {
  transition: all 0.3s ease;
  overflow: hidden;
}

.equipment-category-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.on-hover {
  transform: translateY(-5px);
}

.category-card {
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.category-image {
  position: relative;
}

.category-image::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.equipment-details :deep(h1),
.equipment-details :deep(h2),
.equipment-details :deep(h3),
.equipment-details :deep(h4),
.equipment-details :deep(h5),
.equipment-details :deep(h6) {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.equipment-details :deep(p) {
  margin-bottom: 1rem;
}

.equipment-details :deep(ul),
.equipment-details :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.equipment-details :deep(li) {
  margin-bottom: 0.5rem;
}

/* Responsive Design */
@media (max-width: 960px) {
  .equipment-details {
    padding: 0;
  }
}

@media (max-width: 600px) {
  .equipment-category-badge {
    top: 8px;
    left: 8px;
    font-size: 0.75rem;
    padding: 2px 8px;
  }
}
</style>
