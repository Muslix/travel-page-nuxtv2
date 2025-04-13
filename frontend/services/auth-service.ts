import { useLocalStorage } from '@vueuse/core';

// Token-Speicherung
const AUTH_TOKEN_KEY = 'auth_token';
const USER_DATA_KEY = 'user_data';

// Auth state
const authToken = useLocalStorage(AUTH_TOKEN_KEY, null);
const userData = useLocalStorage(USER_DATA_KEY, null);

/**
 * Auth-Service zum Handling der Authentifizierung
 */
export default {
  /**
   * Login mit Benutzername und Passwort
   */
  async login(username: string, password: string) {
    try {
      // Form-Daten formatieren
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      // API-Aufruf
      const response = await fetch('/api/v1/auth/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login fehlgeschlagen');
      }

      // Token und Benutzerdaten speichern
      const data = await response.json();
      authToken.value = data.access_token;

      // Benutzerdaten abrufen
      await this.fetchUserData();
      
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      authToken.value = null;
      userData.value = null;
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Login fehlgeschlagen'
      };
    }
  },

  /**
   * Benutzerinformationen abrufen
   */
  async fetchUserData() {
    if (!this.isAuthenticated()) {
      return null;
    }

    try {
      const response = await fetch('/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${authToken.value}`
        }
      });

      if (!response.ok) {
        throw new Error('Fehler beim Abrufen der Benutzerdaten');
      }

      const data = await response.json();
      userData.value = data;
      return data;
    } catch (error) {
      console.error('Error fetching user data:', error);
      return null;
    }
  },

  /**
   * Prüft, ob der Benutzer eingeloggt ist
   */
  isAuthenticated() {
    return !!authToken.value;
  },

  /**
   * Prüft, ob der Benutzer Admin-Rechte hat
   */
  isAdmin() {
    return this.isAuthenticated() && userData.value?.is_admin === true;
  },

  /**
   * Gibt das Auth-Token zurück
   */
  getToken() {
    return authToken.value;
  },

  /**
   * Gibt die Benutzerdaten zurück
   */
  getUserData() {
    return userData.value;
  },

  /**
   * Logout - Token und Benutzerdaten löschen
   */
  logout() {
    authToken.value = null;
    userData.value = null;
  }
};
