import authService from '~/services/auth-service';

export default defineNuxtRouteMiddleware((to, from) => {
  // Der Benutzer versucht, auf eine Admin-Seite zuzugreifen
  if (to.path.startsWith('/admin') && to.path !== '/admin/login') {
    // Überprüfen, ob der Benutzer authentifiziert ist
    if (!authService.isAuthenticated()) {
      // Wenn nicht authentifiziert, zur Login-Seite umleiten
      return navigateTo('/admin/login');
    }
    
    // Überprüfen, ob der Benutzer Admin-Rechte hat
    if (!authService.isAdmin()) {
      // Wenn kein Admin, zur Startseite umleiten
      return navigateTo('/');
    }
  }
  
  // Wenn der Benutzer bereits eingeloggt ist und die Login-Seite aufruft, zum Dashboard umleiten
  if (to.path === '/admin/login' && authService.isAuthenticated()) {
    return navigateTo('/admin');
  }
});
