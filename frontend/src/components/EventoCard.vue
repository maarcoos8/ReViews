<template>
  <ion-item button>
    <ion-thumbnail slot="start" v-if="evento.imagen">
      <img :src="evento.imagen" :alt="evento.nombre" />
    </ion-thumbnail>
    <ion-label>
      <h2>{{ evento.nombre }}</h2>
      <p>
        <ion-icon :icon="person"></ion-icon>
        {{ evento.organizador }}
      </p>
      <p>
        <ion-icon :icon="calendar"></ion-icon>
        {{ formatFecha(evento.timestamp) }}
      </p>
      <p>
        <ion-icon :icon="location"></ion-icon>
        {{ evento.lugar }}
      </p>
    </ion-label>
    <ion-button slot="end" fill="outline">
      Ver Detalles
    </ion-button>
  </ion-item>
</template>

<script setup lang="ts">
import { IonItem, IonLabel, IonThumbnail, IonButton, IonIcon } from '@ionic/vue';
import { person, calendar, location } from 'ionicons/icons';
import type { Evento } from '@/interfaces/eventual';

defineProps<{
  evento: Evento;
}>();

const formatFecha = (fecha: string) => {
  return new Date(fecha).toLocaleString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};
</script>

<style scoped>
ion-thumbnail {
  width: 80px;
  height: 80px;
}

ion-label p {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 4px 0;
}

ion-icon {
  font-size: 14px;
}
</style>
