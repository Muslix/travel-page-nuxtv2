<template>
  <v-app>
    <v-navigation-drawer app permanent clipped>
      <v-list>
        <v-list-item to="/admin" title="Dashboard">
          <template #prepend>
            <v-icon>mdi-view-dashboard</v-icon>
          </template>
        </v-list-item>
        
        <v-list-item to="/admin/abenteuer" title="Abenteuer">
          <template #prepend>
            <v-icon>mdi-hiking</v-icon>
          </template>
        </v-list-item>
        
        <v-list-item to="/admin/abenteuer/neu" title="Neues Abenteuer">
          <template #prepend>
            <v-icon>mdi-plus</v-icon>
          </template>
        </v-list-item>
        
        <v-list-item to="/admin/ausruestung" title="Ausrüstung">
          <template #prepend>
            <v-icon>mdi-backpack</v-icon>
          </template>
        </v-list-item>
        
        <v-list-item to="/admin/galerie" title="Galerie">
          <template #prepend>
            <v-icon>mdi-image</v-icon>
          </template>
        </v-list-item>
        
        <v-list-item to="/admin/profile" title="Profile">
          <template #prepend>
            <v-icon>mdi-account</v-icon>
          </template>
        </v-list-item>
      </v-list>
      
      <template #append>
        <div class="pa-2">
          <v-btn block color="error" @click="logout">
            <v-icon left>mdi-logout</v-icon>
            Abmelden
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-app-bar app color="primary" dark clipped-left>
      <v-app-bar-title class="text-h6">Admin-Bereich</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn icon href="/" target="_blank" title="Zur Website">
        <v-icon>mdi-web</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <slot />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import authService from '~/services/auth-service';

const router = useRouter();

function logout() {
  authService.logout();
  router.push('/admin/login');
}
</script>
