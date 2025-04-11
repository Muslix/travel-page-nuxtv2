<template>
  <div>
    <v-container class="fill-height">
      <v-row justify="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark>
              <v-toolbar-title>Admin Login</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form" v-model="isFormValid">
                <v-text-field
                  v-model="username"
                  label="Benutzername"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  :rules="[v => !!v || 'Benutzername ist erforderlich']"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  label="Passwort"
                  prepend-inner-icon="mdi-lock"
                  variant="outlined"
                  :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showPassword ? 'text' : 'password'"
                  @click:append-inner="showPassword = !showPassword"
                  :rules="[v => !!v || 'Passwort ist erforderlich']"
                  required
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="login" :disabled="!isFormValid">
                Anmelden
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const isFormValid = ref(false)

const login = async () => {
  try {
    // In einer echten Anwendung würde hier die API-Anfrage für die Authentifizierung stehen
    // const response = await fetch('/api/auth/login', {...})
    
    // Simuliere erfolgreichen Login
    setTimeout(() => {
      // Speichere Token in localStorage oder besser in einem sicheren Cookie
      localStorage.setItem('admin_token', 'dummy_token')
      // Navigiere zum Dashboard
      router.push('/admin/dashboard')
    }, 1000)
  } catch (error) {
    console.error('Login fehlgeschlagen', error)
    // Hier könntest du eine Fehlermeldung anzeigen
  }
}
</script>
