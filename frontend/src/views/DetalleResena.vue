<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>Detalle de Reseña</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <div v-if="loading" class="loading">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else-if="resena" class="resena-detalle">
        <ion-card>
          <ion-card-header>
            <ion-card-title>{{ resena.nombre_establecimiento }}</ion-card-title>
            <div class="valoracion-header">
              <ion-icon
                v-for="i in 5"
                :key="i"
                :icon="i <= resena.valoracion ? star : starOutline"
                :color="i <= resena.valoracion ? 'warning' : 'medium'"
                size="large"
              ></ion-icon>
              <span class="valoracion-num">{{ resena.valoracion.toFixed(1) }}</span>
            </div>
          </ion-card-header>

          <ion-card-content>
            <ion-list class="info-list">
              <ion-item>
                <ion-icon :icon="locationOutline" slot="start"></ion-icon>
                <ion-label>
                  <h3>Dirección</h3>
                  <p>{{ resena.direccion }}</p>
                </ion-label>
              </ion-item>

              <ion-item>
                <ion-icon :icon="navigateOutline" slot="start"></ion-icon>
                <ion-label>
                  <h3>Coordenadas</h3>
                  <p>Latitud: {{ resena.latitud.toFixed(6) }}</p>
                  <p>Longitud: {{ resena.longitud.toFixed(6) }}</p>
                </ion-label>
              </ion-item>

              <ion-item>
                <ion-icon :icon="personOutline" slot="start"></ion-icon>
                <ion-label>
                  <h3>Autor</h3>
                  <p>{{ resena.nombre_autor }}</p>
                  <p class="email">{{ resena.email_autor }}</p>
                </ion-label>
              </ion-item>

              <ion-item>
                <ion-icon :icon="timeOutline" slot="start"></ion-icon>
                <ion-label>
                  <h3>Token de Autenticación</h3>
                  <p><strong>Emisión:</strong> {{ formatFecha(resena.token_emision) }}</p>
                  <p><strong>Caducidad:</strong> {{ formatFecha(resena.token_caducidad) }}</p>
                </ion-label>
              </ion-item>

              <ion-item>
                <ion-icon :icon="keyOutline" slot="start"></ion-icon>
                <ion-label>
                  <h3>Token OAuth</h3>
                  <p class="token-text">{{ resena.token_oauth }}</p>
                </ion-label>
              </ion-item>
            </ion-list>

            <!-- Imágenes -->
            <div v-if="resena.imagenes && resena.imagenes.length > 0" class="imagenes-section">
              <h3 class="section-title">Imágenes ({{ resena.imagenes.length }})</h3>
              <div class="imagenes-grid">
                <img
                  v-for="(imagen, index) in resena.imagenes"
                  :key="index"
                  :src="imagen"
                  :alt="`Imagen ${index + 1} de ${resena.nombre_establecimiento}`"
                  class="imagen-item"
                  @click="verImagenCompleta(imagen)"
                />
              </div>
            </div>

            <div v-else class="no-imagenes">
              <ion-icon :icon="imagesOutline" size="large"></ion-icon>
              <p>No hay imágenes disponibles</p>
            </div>
          </ion-card-content>
        </ion-card>
      </div>

      <div v-else class="error-state">
        <ion-icon :icon="alertCircleOutline" size="large"></ion-icon>
        <p>No se pudo cargar la reseña</p>
        <ion-button @click="$router.back()">Volver</ion-button>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButtons,
  IonBackButton,
  IonIcon,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonList,
  IonItem,
  IonLabel,
  IonSpinner,
  IonButton,
} from '@ionic/vue';
import {
  star,
  starOutline,
  locationOutline,
  navigateOutline,
  personOutline,
  timeOutline,
  keyOutline,
  imagesOutline,
  alertCircleOutline,
} from 'ionicons/icons';
import { resenaService } from '@/services/resena.service';
import type { Resena } from '@/interfaces/eventual';

const route = useRoute();
const router = useRouter();
const resena = ref<Resena | null>(null);
const loading = ref(true);

const formatFecha = (fecha: string) => {
  return new Date(fecha).toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const verImagenCompleta = (url: string) => {
  window.open(url, '_blank');
};

const cargarResena = async () => {
  try {
    loading.value = true;
    const id = route.params.id as string;
    resena.value = await resenaService.obtenerPorId(id);
  } catch (error) {
    console.error('Error al cargar reseña:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  cargarResena();
});
</script>

<style scoped>
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.resena-detalle {
  padding: 16px;
}

.valoracion-header {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
}

.valoracion-num {
  margin-left: 8px;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--ion-color-warning);
}

.info-list {
  margin-bottom: 24px;
}

.info-list ion-item {
  --padding-start: 0;
  --inner-padding-end: 0;
}

.info-list h3 {
  font-weight: 600;
  color: var(--ion-color-dark);
  margin-bottom: 4px;
}

.info-list p {
  margin: 2px 0;
  color: var(--ion-color-medium);
}

.email {
  font-size: 0.9rem;
  font-style: italic;
}

.token-text {
  font-family: monospace;
  font-size: 0.85rem;
  word-break: break-all;
  background: var(--ion-color-light);
  padding: 8px;
  border-radius: 4px;
  margin-top: 4px;
}

.imagenes-section {
  margin-top: 24px;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--ion-color-dark);
}

.imagenes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.imagen-item {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
  border: 1px solid var(--ion-color-light-shade);
}

.imagen-item:hover {
  transform: scale(1.05);
}

.no-imagenes {
  text-align: center;
  padding: 40px 20px;
  color: var(--ion-color-medium);
}

.no-imagenes ion-icon {
  margin-bottom: 16px;
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 20px;
  color: var(--ion-color-medium);
}

.error-state ion-icon {
  margin-bottom: 16px;
  color: var(--ion-color-danger);
}
</style>
