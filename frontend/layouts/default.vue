<template>
  <v-app>
    <header class="bg-primary text-white">
      <v-app-bar app flat class="px-4">
        <v-app-bar-title>
          <nuxt-link to="/" class="text-white text-decoration-none font-weight-bold">
            Schwob aufm Sattl
          </nuxt-link>
        </v-app-bar-title>
        
        <v-spacer></v-spacer>
        
        <div class="hidden md:flex">
          <v-btn to="/abenteuer" variant="text" class="mx-1">Abenteuer</v-btn>
          <v-btn to="/ausruestung" variant="text" class="mx-1">Ausrüstung</v-btn>
          <v-btn to="/galerie" variant="text" class="mx-1">Galerie</v-btn>
          <v-btn to="/profil" variant="text" class="mx-1">Profil</v-btn>
        </div>
        
        <ThemeSwitcher class="ml-2 mr-2" />
        
        <v-app-bar-nav-icon class="md:hidden" @click="drawer = !drawer"></v-app-bar-nav-icon>
      </v-app-bar>
      
      <v-navigation-drawer v-model="drawer" temporary class="md:hidden">
        <v-list>
          <v-list-item to="/" title="Home"></v-list-item>
          <v-list-item to="/abenteuer" title="Abenteuer"></v-list-item>
          <v-list-item to="/ausruestung" title="Ausrüstung"></v-list-item>
          <v-list-item to="/galerie" title="Galerie"></v-list-item>
          <v-list-item to="/profil" title="Profil"></v-list-item>
          <v-divider class="my-2"></v-divider>
          <v-list-item>
            <template v-slot:prepend>
              <ThemeSwitcher />
            </template>
            <v-list-item-title>Dark Mode</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </header>

    <main>
      <v-container fluid class="px-4 py-6">
        <slot />
      </v-container>
    </main>

    <footer class="bg-gray-800 text-white py-8">
      <v-container>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h3 class="text-xl font-bold mb-4">Schwob aufm Sattl</h3>
            <p>Ein Blog über Bikepacking, Radreisen und Outdoor-Abenteuer</p>
          </div>
          <div>
            <h3 class="text-xl font-bold mb-4">Links</h3>
            <ul>
              <li><nuxt-link to="/" class="text-white hover:text-accent">Home</nuxt-link></li>
              <li><nuxt-link to="/abenteuer" class="text-white hover:text-accent">Abenteuer</nuxt-link></li>
              <li><nuxt-link to="/ausruestung" class="text-white hover:text-accent">Ausrüstung</nuxt-link></li>
              <li><nuxt-link to="/galerie" class="text-white hover:text-accent">Galerie</nuxt-link></li>
            </ul>
          </div>
          <div>
            <h3 class="text-xl font-bold mb-4">Folge mir</h3>
            <div class="flex space-x-4">
              <a href="#" class="text-white hover:text-accent"><v-icon>mdi-instagram</v-icon></a>
              <a href="#" class="text-white hover:text-accent"><v-icon>mdi-youtube</v-icon></a>
              <a href="#" class="text-white hover:text-accent"><v-icon>mdi-facebook</v-icon></a>
            </div>
          </div>
        </div>
        <div class="mt-8 text-center">
          <p>&copy; {{ new Date().getFullYear() }} Schwob aufm Sattl. Alle Rechte vorbehalten.</p>
        </div>
      </v-container>
    </footer>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const drawer = ref(false);
</script>

<style>
/* Globale Styles */
body {
  @apply bg-gray-50;
}
</style>
