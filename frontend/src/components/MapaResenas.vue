<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Interfaz genérica para puntos en el mapa
interface PuntoMapa {
  id: string;
  nombre: string;
  latitud: number;
  longitud: number;
  lugar?: string;
}

// Fix para los iconos de Leaflet en producción usando CDN
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const props = defineProps<{
  eventos: PuntoMapa[];
  centro: { lat: number; lon: number };
}>();

const mapContainer = ref<HTMLElement | null>(null);
let map: L.Map | null = null;
const markers: L.Marker[] = [];

onMounted(() => {
  if (mapContainer.value) {
    // Inicializar mapa
    map = L.map(mapContainer.value).setView([props.centro.lat, props.centro.lon], 12);

    // Agregar capa de tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
    }).addTo(map);

    // Agregar marcadores
    agregarMarcadores();
    
    // Forzar que el mapa se ajuste al contenedor
    setTimeout(() => {
      if (map) {
        map.invalidateSize();
      }
    }, 100);
  }
});

watch(
  () => [props.eventos, props.centro],
  () => {
    if (map) {
      // Centrar el mapa
      map.setView([props.centro.lat, props.centro.lon], 12);
      
      // Actualizar marcadores
      agregarMarcadores();
    }
  },
  { deep: true }
);

const agregarMarcadores = () => {
  // Limpiar marcadores existentes
  markers.forEach((marker) => marker.remove());
  markers.length = 0;

  if (!map) return;

  // Agregar nuevos marcadores
  props.eventos.forEach((evento: Evento) => {
    const marker = L.marker([evento.latitud, evento.longitud]).addTo(map!);
    marker.bindPopup(`
      <div>
        <h3>${evento.nombre}</h3>
        <p><strong>Organizador:</strong> ${evento.organizador}</p>
        <p><strong>Fecha:</strong> ${new Date(evento.timestamp).toLocaleString()}</p>
        <p><strong>Lugar:</strong> ${evento.lugar}</p>
      </div>
    `);
    markers.push(marker);
  });
};
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
  position: relative;
}

.map-container :deep(.leaflet-container) {
  width: 100%;
  height: 100%;
}
</style>
