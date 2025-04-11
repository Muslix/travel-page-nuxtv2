<template>
  <div>
    <v-container>
      <h1 class="text-h3 mb-5">Admin Dashboard</h1>
      
      <!-- Statistik-Karten -->
      <v-row class="mb-6">
        <v-col cols="12" md="4">
          <v-card color="primary" dark class="pa-3">
            <v-card-text>
              <div class="text-h4 mb-2">12</div>
              <div>Veröffentlichte Abenteuer</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card color="secondary" dark class="pa-3">
            <v-card-text>
              <div class="text-h4 mb-2">24</div>
              <div>Ausrüstungsgegenstände</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card color="accent" dark class="pa-3">
            <v-card-text>
              <div class="text-h4 mb-2">56</div>
              <div>Bilder in der Galerie</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Admin-Aktionen -->
      <v-row class="mb-6">
        <v-col cols="12">
          <v-card>
            <v-card-title>Schnellzugriff</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="6" md="3">
                  <v-btn color="primary" block to="/admin/abenteuer/neu" height="100">
                    <v-icon size="large" class="mb-2">mdi-plus</v-icon>
                    <div>Neues Abenteuer</div>
                  </v-btn>
                </v-col>
                <v-col cols="6" md="3">
                  <v-btn color="secondary" block to="/admin/ausruestung/neu" height="100">
                    <v-icon size="large" class="mb-2">mdi-bike</v-icon>
                    <div>Neue Ausrüstung</div>
                  </v-btn>
                </v-col>
                <v-col cols="6" md="3">
                  <v-btn color="accent" block to="/admin/galerie/upload" height="100">
                    <v-icon size="large" class="mb-2">mdi-image-multiple</v-icon>
                    <div>Bilder hochladen</div>
                  </v-btn>
                </v-col>
                <v-col cols="6" md="3">
                  <v-btn color="info" block to="/admin/profil" height="100">
                    <v-icon size="large" class="mb-2">mdi-account-edit</v-icon>
                    <div>Profil bearbeiten</div>
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Neueste Abenteuer -->
      <v-card class="mb-6">
        <v-card-title class="d-flex justify-space-between">
          <span>Neueste Abenteuer</span>
          <v-btn color="primary" size="small" to="/admin/abenteuer">Alle anzeigen</v-btn>
        </v-card-title>
        <v-card-text>
          <v-table>
            <thead>
              <tr>
                <th>Titel</th>
                <th>Datum</th>
                <th>Region</th>
                <th>Status</th>
                <th>Aktionen</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="n in 5" :key="n">
                <td>Abenteuer {{ n }}</td>
                <td>{{ new Date().toLocaleDateString() }}</td>
                <td>Region {{ n }}</td>
                <td>
                  <v-chip 
                    :color="n % 2 === 0 ? 'success' : 'warning'" 
                    size="small"
                  >
                    {{ n % 2 === 0 ? 'Veröffentlicht' : 'Entwurf' }}
                  </v-chip>
                </td>
                <td>
                  <v-btn icon size="small" color="primary" variant="text">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon size="small" color="error" variant="text">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
      
      <!-- Letzte Aktivitäten -->
      <v-card>
        <v-card-title>Letzte Aktivitäten</v-card-title>
        <v-card-text>
          <v-timeline density="compact" align="start">
            <v-timeline-item
              v-for="n in 5"
              :key="n"
              dot-color="primary"
              size="small"
            >
              <div class="mb-2">
                <strong>Aktivität {{ n }}</strong>
                <div class="text-caption">vor {{ n }} Stunden</div>
              </div>
              <div>Beschreibung der Aktivität {{ n }}.</div>
            </v-timeline-item>
          </v-timeline>
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
// Dashboard-Logik
</script>
