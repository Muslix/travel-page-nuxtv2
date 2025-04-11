<template>
  <div>
    <v-container>
      <h1 class="text-h3 mb-5">Neues Abenteuer erstellen</h1>
      
      <v-form ref="form" @submit.prevent="saveAdventure">
        <v-card class="mb-4">
          <v-card-title>Allgemeine Informationen</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="8">
                <v-text-field
                  v-model="adventure.title"
                  label="Titel"
                  variant="outlined"
                  required
                  :rules="[v => !!v || 'Titel ist erforderlich']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                  v-model="adventure.status"
                  label="Status"
                  :items="['Entwurf', 'Veröffentlicht', 'Geplant']"
                  variant="outlined"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="adventure.description"
                  label="Kurzbeschreibung"
                  variant="outlined"
                  rows="3"
                  required
                  :rules="[v => !!v || 'Beschreibung ist erforderlich']"
                ></v-textarea>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="adventure.location"
                  label="Region/Ort"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field
                  v-model="adventure.distance"
                  label="Distanz (km)"
                  variant="outlined"
                  type="number"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field
                  v-model="adventure.duration"
                  label="Dauer (Tage)"
                  variant="outlined"
                  type="number"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="adventure.startDate"
                  label="Startdatum"
                  variant="outlined"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="adventure.endDate"
                  label="Enddatum"
                  variant="outlined"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-combobox
                  v-model="adventure.tags"
                  label="Tags"
                  variant="outlined"
                  multiple
                  chips
                  :items="['Bikepacking', 'Graveln', 'Mountainbike', 'Rennrad', 'Mehrtägig', 'Tagestour', 'Alpen', 'Schwarzwald', 'Schwäbische Alb']"
                ></v-combobox>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
        
        <v-card class="mb-4">
          <v-card-title>Cover-Bild & Galerie</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-file-input
                  v-model="coverImage"
                  label="Cover-Bild"
                  variant="outlined"
                  accept="image/*"
                  prepend-icon="mdi-camera"
                  show-size
                ></v-file-input>
              </v-col>
              
              <v-col cols="12">
                <v-file-input
                  v-model="galleryImages"
                  label="Bilder für Galerie"
                  variant="outlined"
                  accept="image/*"
                  prepend-icon="mdi-image-multiple"
                  multiple
                  show-size
                  counter
                ></v-file-input>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
        
        <v-card class="mb-4">
          <v-card-title>Routeninformationen</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-file-input
                  v-model="gpxFile"
                  label="GPX-Datei hochladen"
                  variant="outlined"
                  accept=".gpx"
                  prepend-icon="mdi-map"
                  show-size
                ></v-file-input>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="adventure.elevation"
                  label="Höhenmeter"
                  variant="outlined"
                  type="number"
                  suffix="m"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                  v-model="adventure.difficulty"
                  label="Schwierigkeitsgrad"
                  :items="['Leicht', 'Mittel', 'Schwer', 'Extrem']"
                  variant="outlined"
                ></v-select>
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                  v-model="adventure.surface"
                  label="Untergrund"
                  :items="['Asphalt', 'Schotter', 'Trail', 'Gemischt']"
                  variant="outlined"
                ></v-select>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
        
        <v-card class="mb-4">
          <v-card-title>Inhalt</v-card-title>
          <v-card-text>
            <v-textarea
              v-model="adventure.content"
              label="Ausführliche Beschreibung (Markdown unterstützt)"
              variant="outlined"
              rows="15"
              required
              :rules="[v => !!v || 'Inhalt ist erforderlich']"
            ></v-textarea>
          </v-card-text>
        </v-card>
        
        <v-card class="mb-6">
          <v-card-title>Ausrüstung & Tipps</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-textarea
                  v-model="adventure.equipment"
                  label="Verwendete Ausrüstung"
                  variant="outlined"
                  rows="5"
                ></v-textarea>
              </v-col>
              <v-col cols="12" md="6">
                <v-textarea
                  v-model="adventure.tips"
                  label="Tipps & Empfehlungen"
                  variant="outlined"
                  rows="5"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
        
        <div class="d-flex justify-end mb-6">
          <v-btn color="error" variant="text" class="me-4" to="/admin/dashboard">
            Abbrechen
          </v-btn>
          <v-btn color="success" type="submit">
            Abenteuer speichern
          </v-btn>
        </div>
      </v-form>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Formular-Daten
const adventure = ref({
  title: '',
  description: '',
  status: 'Entwurf',
  location: '',
  distance: null,
  duration: null,
  startDate: '',
  endDate: '',
  tags: [],
  elevation: null,
  difficulty: 'Mittel',
  surface: 'Gemischt',
  content: '',
  equipment: '',
  tips: ''
})

// Datei-Uploads
const coverImage = ref(null)
const galleryImages = ref([])
const gpxFile = ref(null)

// Speichern des Abenteuers
const saveAdventure = async () => {
  try {
    // Hier würde die API-Anfrage zum Speichern des Abenteuers stehen
    // Einschließlich Upload der Bilder und GPX-Datei
    
    // Simulierter Erfolg
    console.log('Abenteuer gespeichert:', adventure.value)
    
    // Zurück zum Dashboard navigieren
    setTimeout(() => {
      router.push('/admin/dashboard')
    }, 1000)
  } catch (error) {
    console.error('Fehler beim Speichern des Abenteuers', error)
  }
}
</script>
