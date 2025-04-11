<template>
  <div>
    <v-container>
      <h1 class="text-h3 mb-5">Abenteuer & Touren</h1>
      
      <!-- Filter & Sortierung -->
      <v-row class="mb-5">
        <v-col cols="12" md="6">
          <v-select
            label="Sortieren nach"
            :items="['Neueste zuerst', 'Älteste zuerst', 'Längste Strecke', 'Kürzeste Strecke']"
            variant="outlined"
            density="comfortable"
          ></v-select>
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            label="Filtern nach Region"
            :items="['Alle Regionen', 'Alpen', 'Schwarzwald', 'Schwäbische Alb', 'Bodensee']"
            variant="outlined"
            density="comfortable"
          ></v-select>
        </v-col>
      </v-row>
      
      <!-- Abenteuer Grid -->
      <v-row>
        <v-col cols="12" md="6" lg="4" v-for="n in 6" :key="n">
          <v-card class="mb-4" :to="`/abenteuer/${n}`">
            <v-img
              src="https://images.unsplash.com/photo-1571988840298-3b5301d5109b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1467&q=80"
              height="250"
              cover
            ></v-img>
            <v-card-title>Abenteuer {{ n }}</v-card-title>
            <v-card-subtitle>
              <v-icon size="small" color="primary">mdi-map-marker</v-icon> Region | 
              <v-icon size="small" color="primary">mdi-calendar</v-icon> Mai 2025
            </v-card-subtitle>
            <v-card-text>
              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam lobortis, nisi vitae vestibulum commodo.</p>
              <v-chip class="mr-2 mt-2" color="primary" size="small" variant="outlined">Bikepacking</v-chip>
              <v-chip class="mr-2 mt-2" color="secondary" size="small" variant="outlined">Alpen</v-chip>
              <v-chip class="mr-2 mt-2" color="accent" size="small" variant="outlined">Mehrtägig</v-chip>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" variant="text">Mehr lesen</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Pagination -->
      <div class="text-center mt-5">
        <v-pagination
          v-model="page"
          :length="3"
          color="primary"
        ></v-pagination>
      </div>
    </v-container>
  </div>
</template>

<script setup>
const page = ref(1)
</script>
