<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <v-card class="login-card pa-6 mx-auto" max-width="450px">
      <v-card-title class="text-center text-h4 font-weight-bold mb-4">
        Admin Login
      </v-card-title>
      
      <v-card-text>
        <v-alert v-if="loginError" type="error" class="mb-4">
          {{ loginError }}
        </v-alert>
        
        <v-form @submit.prevent="handleLogin" ref="form">
          <v-text-field
            v-model="username"
            label="Benutzername"
            prepend-icon="mdi-account"
            :rules="[required]"
            autocomplete="username"
          ></v-text-field>
          
          <v-text-field
            v-model="password"
            label="Passwort"
            prepend-icon="mdi-lock"
            :type="showPassword ? 'text' : 'password'"
            :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append="showPassword = !showPassword"
            :rules="[required]"
            autocomplete="current-password"
          ></v-text-field>
          
          <div class="d-flex justify-end mt-4">
            <v-btn
              type="submit"
              color="primary"
              :loading="loading"
              block
            >
              Anmelden
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
      
      <v-card-actions class="justify-center">
        <v-btn
          variant="text"
          color="primary"
          to="/"
        >
          Zurück zur Website
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
import authService from '~/services/auth-service';

// Reaktive Zustände
const username = ref('');
const password = ref('');
const showPassword = ref(false);
const loading = ref(false);
const loginError = ref('');
const form = ref(null);

// Validierung
const required = (v) => !!v || 'Dieses Feld wird benötigt';

// Login-Handler
async function handleLogin() {
  // Formular validieren
  const isValid = await form.value?.validate();
  if (!isValid?.valid) return;
  
  loading.value = true;
  loginError.value = '';
  
  try {
    // Login mit dem Auth-Service
    const result = await authService.login(username.value, password.value);
    
    if (result.success) {
      // Bei Erfolg zum Admin-Dashboard navigieren
      navigateTo('/admin');
    } else {
      // Fehler anzeigen
      loginError.value = result.error || 'Login fehlgeschlagen. Bitte überprüfen Sie Ihre Anmeldedaten.';
    }
  } catch (error) {
    console.error('Login error:', error);
    loginError.value = 'Ein unerwarteter Fehler ist aufgetreten.';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
</style>
