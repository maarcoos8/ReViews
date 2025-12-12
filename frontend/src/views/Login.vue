<template>
  <ion-page>
    <ion-content :fullscreen="true" class="ion-padding">
      <div class="login-container">
        <div class="logo-section">
          <ion-icon :icon="starOutline" class="logo-icon"></ion-icon>
          <h1>ReViews</h1>
          <p class="subtitle">Comparte y descubre reseñas de establecimientos</p>
        </div>

        <div class="features">
          <div class="feature">
            <ion-icon :icon="locationOutline"></ion-icon>
            <span>Descubre establecimientos cercanos</span>
          </div>
          <div class="feature">
            <ion-icon :icon="starHalfOutline"></ion-icon>
            <span>Lee y escribe reseñas</span>
          </div>
          <div class="feature">
            <ion-icon :icon="imagesOutline"></ion-icon>
            <span>Comparte fotos de los lugares</span>
          </div>
        </div>

        <ion-button expand="block" @click="handleLogin" :disabled="loading">
          <ion-icon slot="start" :icon="logoGoogle"></ion-icon>
          Iniciar sesión con Google
        </ion-button>

        <p class="info-text">
          Al iniciar sesión, aceptas nuestros términos y condiciones
        </p>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonContent, IonButton, IonIcon } from '@ionic/vue';
import { starOutline, starHalfOutline, locationOutline, imagesOutline, logoGoogle } from 'ionicons/icons';
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const loading = ref(false);

function handleLogin() {
  loading.value = true;
  authStore.loginWithGoogle();
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.logo-section {
  text-align: center;
  margin-bottom: 3rem;
}

.logo-icon {
  font-size: 80px;
  color: var(--ion-color-primary);
  margin-bottom: 1rem;
}

h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0;
  color: var(--ion-color-primary);
}

.subtitle {
  color: var(--ion-color-medium);
  font-size: 1.1rem;
  margin-top: 0.5rem;
}

.features {
  width: 100%;
  margin-bottom: 2rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 0.5rem;
  background: var(--ion-color-light);
  border-radius: 8px;
}

.feature ion-icon {
  font-size: 24px;
  color: var(--ion-color-primary);
}

ion-button {
  margin-top: 1rem;
  --border-radius: 8px;
  height: 50px;
  font-weight: 600;
}

.info-text {
  margin-top: 2rem;
  font-size: 0.875rem;
  color: var(--ion-color-medium);
  text-align: center;
}
</style>
