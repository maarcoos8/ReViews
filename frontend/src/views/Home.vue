<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Reseñas</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <div class="container">
        <!-- Grid: Lista + Mapa -->
        <div class="main-grid">
          <!-- Lista de reseñas -->
          <div class="resenas-section">
            <div class="create-button-container">
              <ion-button expand="block" @click="crearResena">
                <ion-icon :icon="addOutline" slot="start"></ion-icon>
                Crear Reseña
              </ion-button>
            </div>
            <ion-list v-if="resenas.length > 0">
              <ion-list-header>
                <ion-label>Reseñas ({{ total }})</ion-label>
              </ion-list-header>
              <ion-item
                v-for="resena in resenas"
                :key="resena._id"
                button
                @click="verDetalle(resena._id)"
                class="resena-item"
              >
                <div class="resena-content">
                  <h3>{{ resena.nombre_establecimiento }}</h3>
                  <p class="direccion">
                    <ion-icon :icon="locationOutline" size="small"></ion-icon>
                    {{ resena.direccion }}
                  </p>
                  <p class="coordenadas">
                    Coordenadas: {{ resena.latitud.toFixed(4) }}, {{ resena.longitud.toFixed(4) }}
                  </p>
                  <div class="valoracion">
                    <ion-icon
                      v-for="i in 5"
                      :key="i"
                      :icon="i <= resena.valoracion ? star : starOutline"
                      :color="i <= resena.valoracion ? 'warning' : 'medium'"
                    ></ion-icon>
                    <span class="valoracion-num">{{ resena.valoracion.toFixed(1) }}</span>
                  </div>
                </div>
              </ion-item>
            </ion-list>

            <div v-else-if="!loading" class="empty-state">
              <ion-icon :icon="starOutline" size="large"></ion-icon>
              <p>No hay reseñas disponibles</p>
            </div>

            <div v-if="loading" class="loading">
              <ion-spinner></ion-spinner>
            </div>
          </div>

          <!-- Mapa -->
          <div class="map-section">
            <div class="search-map-container">
              <div class="search-box">
                <ion-input
                  v-model="busquedaUbicacion"
                  placeholder="Buscar ubicación (ej: Madrid, España)"
                  @keyup.enter="buscarUbicacion"
                ></ion-input>
                <ion-button @click="buscarUbicacion" :disabled="loadingUbicacion">
                  <ion-icon v-if="!loadingUbicacion" :icon="searchOutline" slot="start"></ion-icon>
                  <ion-spinner v-else name="circular" slot="start"></ion-spinner>
                  Buscar
                </ion-button>
              </div>
            </div>
            <div class="map-container">
              <MapaResenas :eventos="resenasParaMapa" :centro="centroMapa" :key="mapKey" />
            </div>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted, onActivated, computed } from 'vue';
import { useRouter } from 'vue-router';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonList,
  IonListHeader,
  IonLabel,
  IonIcon,
  IonSpinner,
  IonItem,
  IonInput,
} from '@ionic/vue';
import { star, starOutline, locationOutline, searchOutline, addOutline } from 'ionicons/icons';
import { useAuthStore } from '@/stores/auth';
import { resenaService } from '@/services/resena.service';
import type { Resena } from '@/interfaces/eventual';
import MapaResenas from '@/components/MapaResenas.vue';

const router = useRouter();
const authStore = useAuthStore();
const resenas = ref<Resena[]>([]);
const total = ref(0);
const loading = ref(true);
const busquedaUbicacion = ref('');
const loadingUbicacion = ref(false);
const mapKey = ref(0);

// Adaptar reseñas para el componente de mapa
const resenasParaMapa = computed(() => {
  return resenas.value.map(r => ({
    id: r._id,
    nombre: r.nombre_establecimiento,
    latitud: r.latitud,
    longitud: r.longitud,
    lugar: r.direccion,
    timestamp: r.created_at,
    organizador: r.email_autor,
    created_at: r.created_at,
  }));
});

// Centro del mapa (puede cambiar con la búsqueda)
const centroMapa = ref({ lat: 40.4168, lon: -3.7038 }); // Madrid por defecto

const cargarResenas = async () => {
  try {
    loading.value = true;
    const respuesta = await resenaService.obtenerTodas();
    resenas.value = respuesta.resenas;
    total.value = respuesta.total;
  } catch (error) {
    console.error('Error al cargar reseñas:', error);
  } finally {
    loading.value = false;
  }
};

const verDetalle = (id: string) => {
  router.push(`/resena/${id}`);
};

const crearResena = () => {
  router.push('/crear-resena');
};

const buscarUbicacion = async () => {
  if (!busquedaUbicacion.value.trim()) return;
  
  try {
    loadingUbicacion.value = true;
    // Usar la API de Nominatim directamente desde el frontend
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(busquedaUbicacion.value)}&format=json&limit=1`;
    
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'ReViews/1.0'
      }
    });
    
    if (!response.ok) {
      throw new Error('Error al buscar ubicación');
    }
    
    const results = await response.json();
    
    if (results.length > 0) {
      const { lat, lon } = results[0];
      centroMapa.value = { lat: parseFloat(lat), lon: parseFloat(lon) };
      // Forzar recarga del mapa
      mapKey.value++;
    } else {
      alert('No se encontró la ubicación. Intenta con otro nombre.');
    }
  } catch (error) {
    console.error('Error al buscar ubicación:', error);
    alert('Error al buscar la ubicación');
  } finally {
    loadingUbicacion.value = false;
  }
};

onMounted(() => {
  cargarResenas().then(() => {
    // Centrar en la primera reseña si existe
    if (resenas.value.length > 0) {
      centroMapa.value = {
        lat: resenas.value[0].latitud,
        lon: resenas.value[0].longitud,
      };
    }
  });
});

// Recargar las reseñas cada vez que volvemos a esta página (importante después de crear)
onActivated(() => {
  cargarResenas();
});
</script>

<style scoped>
.container {
  padding: 16px;
  height: 100%;
}

.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  height: calc(100vh - 120px);
}

@media (max-width: 768px) {
  .main-grid {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 400px;
  }
}

.resenas-section {
  overflow-y: auto;
  height: 100%;
}

.create-button-container {
  padding: 16px;
  background: white;
  border-bottom: 1px solid var(--ion-color-light-shade);
  position: sticky;
  top: 0;
  z-index: 10;
}

.map-section {
  position: sticky;
  top: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.search-map-container {
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-box {
  display: flex;
  gap: 8px;
  align-items: center;
}

.search-box ion-input {
  flex: 1;
  --background: var(--ion-color-light);
  --border-radius: 8px;
  --padding-start: 12px;
  --padding-end: 12px;
}

.search-box ion-button {
  --padding-start: 16px;
  --padding-end: 16px;
}

.map-container {
  flex: 1;
  min-height: 400px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--ion-color-light-shade);
}

.resena-item {
  --padding-start: 16px;
  --padding-end: 16px;
  margin-bottom: 8px;
}

.resena-content {
  width: 100%;
  padding: 8px 0;
}

.resena-content h3 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--ion-color-dark);
}

.direccion {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 4px 0;
  font-size: 0.9rem;
  color: var(--ion-color-medium);
}

.coordenadas {
  margin: 4px 0;
  font-size: 0.85rem;
  color: var(--ion-color-medium-shade);
  font-family: monospace;
}

.valoracion {
  display: flex;
  align-items: center;
  gap: 2px;
  margin-top: 8px;
}

.valoracion-num {
  margin-left: 8px;
  font-weight: 600;
  color: var(--ion-color-warning);
}

.token-oauth {
  margin-top: 8px;
  font-size: 0.75rem;
  color: var(--ion-color-medium);
  word-break: break-all;
  line-height: 1.3;
}

.token-oauth strong {
  color: var(--ion-color-dark);
}

.empty-state {
  text-align: center;
  padding: 48px 16px;
  color: var(--ion-color-medium);
}

.empty-state ion-icon {
  margin-bottom: 16px;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 32px;
}
</style>
