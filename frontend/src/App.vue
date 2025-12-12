<template>
  <ion-app>
    <ion-header v-if="authStore.isAuthenticated">
      <ion-toolbar>
        <ion-title>
          <span @click="goHome" class="clickable-title">ReViews</span>
        </ion-title>
        <ion-buttons slot="end">
          <ion-button @click="authStore.logout" color="danger" fill="solid">
            <ion-icon :icon="logOut" slot="start"></ion-icon>
            Logout
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-router-outlet />
  </ion-app>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { IonApp, IonRouterOutlet, IonHeader, IonToolbar, IonTitle, IonButtons, IonButton, IonIcon } from '@ionic/vue';
import { logOut } from 'ionicons/icons';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import ThemeService from '@/services/shared/theme.service';

const router = useRouter();

const authStore = useAuthStore();

const goHome = () => {
  router.push('/');
};

// Inicializar tema y cargar usuario al iniciar la aplicación
onMounted(async () => {
  // FORZAR tema claro siempre (eliminar cualquier configuración anterior)
  localStorage.removeItem('selected-theme');
  ThemeService.setTheme('light');
  console.log('Tema forzado a claro');
  
  await authStore.loadUser();
});
</script>

<style scoped>
.clickable-title {
  cursor: pointer;
  user-select: none;
}

.clickable-title:hover {
  opacity: 0.8;
}
</style>
