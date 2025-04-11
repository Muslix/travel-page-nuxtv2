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
            v-model="email"
            label="E-Mail"
            prepend-icon="mdi-email"
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

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

definePageMeta({
  layout: false,  // Kein Layout für die Login-Seite
});

const router = useRouter();
const email = ref('');
const password = ref('');
const showPassword = ref(false);
const loading = ref(false);
const loginError = ref('');
const form = ref(null);

const required = (v: string) => !!v || 'Dieses Feld ist erforderlich';

async function handleLogin() {
  if (!form.value) return;
  
  const results = await form.value.validate();
  const valid = !results.errors.length;
  
  if (!valid) return;
  
  loading.value = true;
  loginError.value = '';
  
  try {
    // Hier später mit echtem Backend-Aufruf ersetzen
    // Beispiel für ein einfaches Login (später durch echte API ersetzen)
    if (email.value === 'admin@example.com' && password.value === 'password') {
      // Token im localStorage speichern (später durch echte Auth ersetzen)
      localStorage.setItem('admin_token', 'dummy_token');
      router.push('/admin');
    } else {
      loginError.value = 'Ungültige Anmeldedaten';
    }
  } catch (error) {
    console.error('Login error:', error);
    loginError.value = 'Es ist ein Fehler aufgetreten. Bitte versuche es später erneut.';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-card {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
</style>
