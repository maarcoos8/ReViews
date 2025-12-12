<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="callback-container">
        <ion-spinner name="crescent"></ion-spinner>
        <p>{{ message }}</p>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonContent, IonSpinner } from '@ionic/vue';
import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const message = ref('Procesando autenticación...');

onMounted(async () => {
  const token = route.query.token as string;
  const error = route.query.error as string;

  if (error) {
    message.value = 'Error en la autenticación';
    setTimeout(() => router.push('/'), 2000);
    return;
  }

  if (token) {
    try {
      await authStore.handleOAuthCallback(token);
      message.value = 'Autenticación exitosa';
      setTimeout(() => router.push('/'), 1000);
    } catch (err) {
      message.value = 'Error al iniciar sesión';
      setTimeout(() => router.push('/'), 2000);
    }
  } else {
    message.value = 'Token no válido';
    setTimeout(() => router.push('/'), 2000);
  }
});
</script>

<style scoped>
.callback-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  gap: 1rem;
}

ion-spinner {
  transform: scale(1.5);
  color: var(--ion-color-primary);
}

p {
  color: var(--ion-color-medium);
  font-size: 1.1rem;
}
</style>
