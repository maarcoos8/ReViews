<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>Historial de Sesiones</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <div v-if="loading" class="loading">
        <ion-spinner></ion-spinner>
      </div>

      <ion-list v-else-if="logs.length > 0">
        <ion-list-header>
          <ion-label>Total de sesiones: {{ logs.length }}</ion-label>
        </ion-list-header>

        <ion-item v-for="log in logs" :key="log.id">
          <ion-label>
            <h2>{{ log.usuario }}</h2>
            <p>
              <strong>Login:</strong> {{ formatFecha(log.timestamp) }}
            </p>
            <p>
              <strong>Caducidad:</strong> {{ formatFecha(log.caducidad) }}
            </p>
            <p class="token-preview">
              <strong>Token:</strong> {{ log.token.substring(0, 50) }}...
            </p>
          </ion-label>
        </ion-item>
      </ion-list>

      <div v-else class="empty-state">
        <ion-icon :icon="document" size="large"></ion-icon>
        <p>No hay registros de sesiones</p>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButtons,
  IonBackButton,
  IonList,
  IonListHeader,
  IonItem,
  IonLabel,
  IonSpinner,
  IonIcon,
} from '@ionic/vue';
import { document } from 'ionicons/icons';
import sessionLogService from '@/services/session-log.service';
import type { SessionLog } from '@/interfaces/eventual';

const logs = ref<SessionLog[]>([]);
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  try {
    logs.value = await sessionLogService.obtenerLogs();
  } catch (error) {
    console.error('Error al cargar logs:', error);
  } finally {
    loading.value = false;
  }
});

const formatFecha = (fecha: string) => {
  return new Date(fecha).toLocaleString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
};
</script>

<style scoped>
.loading {
  display: flex;
  justify-content: center;
  padding: 48px;
}

.empty-state {
  text-align: center;
  padding: 48px 16px;
  color: var(--ion-color-medium);
}

.empty-state ion-icon {
  margin-bottom: 16px;
}

.token-preview {
  font-size: 12px;
  font-family: monospace;
  word-break: break-all;
}
</style>
