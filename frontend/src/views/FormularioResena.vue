<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>Crear Reseña</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <div class="form-container">
        <form @submit.prevent="guardarResena">
          <ion-card>
            <ion-card-header>
              <ion-card-title>Nueva Reseña</ion-card-title>
            </ion-card-header>

            <ion-card-content>
              <!-- Nombre del establecimiento -->
              <ion-item>
                <ion-label position="stacked">Nombre del Establecimiento *</ion-label>
                <ion-input
                  v-model="formData.nombre_establecimiento"
                  placeholder="Ej: Restaurante El Buen Sabor"
                  required
                ></ion-input>
              </ion-item>

              <!-- Dirección -->
              <ion-item>
                <ion-label position="stacked">Dirección *</ion-label>
                <ion-input
                  v-model="formData.direccion"
                  placeholder="Ej: Calle Mayor 123, Madrid"
                  required
                ></ion-input>
              </ion-item>

              <!-- Valoración -->
              <ion-item>
                <ion-label position="stacked">Valoración (0-5) *</ion-label>
                <div class="rating-container">
                  <ion-icon
                    v-for="i in 5"
                    :key="i"
                    :icon="i <= formData.valoracion ? star : starOutline"
                    :color="i <= formData.valoracion ? 'warning' : 'medium'"
                    size="large"
                    class="star-clickable"
                    @click="formData.valoracion = i"
                  ></ion-icon>
                  <span class="rating-value">{{ formData.valoracion.toFixed(1) }}</span>
                </div>
              </ion-item>

              <!-- Selector de imágenes -->
              <ion-item>
                <ion-label position="stacked">Imágenes</ion-label>
                <input
                  type="file"
                  ref="fileInput"
                  multiple
                  accept="image/*"
                  @change="handleFileSelect"
                  style="display: none"
                />
                <ion-button @click="$refs.fileInput.click()" expand="block" fill="outline">
                  <ion-icon :icon="imagesOutline" slot="start"></ion-icon>
                  Seleccionar Imágenes
                </ion-button>
              </ion-item>

              <!-- Preview de imágenes seleccionadas -->
              <div v-if="selectedFiles.length > 0" class="images-preview">
                <p class="preview-title">Imágenes seleccionadas: {{ selectedFiles.length }}</p>
                <div class="preview-grid">
                  <div v-for="(file, index) in selectedFiles" :key="index" class="preview-item">
                    <img :src="getFilePreview(file)" :alt="`Preview ${index + 1}`" />
                    <ion-button
                      fill="clear"
                      size="small"
                      color="danger"
                      class="remove-btn"
                      @click="removeFile(index)"
                    >
                      <ion-icon :icon="closeCircleOutline"></ion-icon>
                    </ion-button>
                  </div>
                </div>
              </div>

              <!-- Botón guardar -->
              <ion-button
                expand="block"
                type="submit"
                :disabled="loading || !isFormValid"
                class="save-button"
              >
                <ion-spinner v-if="loading" name="circular"></ion-spinner>
                <ion-icon v-else :icon="saveOutline" slot="start"></ion-icon>
                {{ loading ? 'Guardando...' : 'Guardar Reseña' }}
              </ion-button>

              <!-- Mensajes de error -->
              <ion-text v-if="errorMessage" color="danger" class="error-message">
                <p>{{ errorMessage }}</p>
              </ion-text>
            </ion-card-content>
          </ion-card>
        </form>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButtons,
  IonBackButton,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonIcon,
  IonSpinner,
  IonText,
} from '@ionic/vue';
import {
  star,
  starOutline,
  imagesOutline,
  saveOutline,
  closeCircleOutline,
} from 'ionicons/icons';
import { resenaService } from '@/services/resena.service';
import type { ResenaCreate } from '@/interfaces/eventual';

const router = useRouter();
const fileInput = ref<HTMLInputElement | null>(null);
const loading = ref(false);
const errorMessage = ref('');
const selectedFiles = ref<File[]>([]);

const formData = ref<ResenaCreate>({
  nombre_establecimiento: '',
  direccion: '',
  latitud: 0,
  longitud: 0,
  valoracion: 0,
  imagenes: [],
});

// Función para resetear el formulario
const resetearFormulario = () => {
  formData.value = {
    nombre_establecimiento: '',
    direccion: '',
    latitud: 0,
    longitud: 0,
    valoracion: 0,
    imagenes: [],
  };
  selectedFiles.value = [];
  errorMessage.value = '';
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

// Resetear el formulario al montar el componente
onMounted(() => {
  resetearFormulario();
});

const isFormValid = computed(() => {
  return (
    formData.value.nombre_establecimiento.trim() !== '' &&
    formData.value.direccion.trim() !== '' &&
    formData.value.valoracion > 0
  );
});

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files) {
    selectedFiles.value = Array.from(target.files);
  }
};

const getFilePreview = (file: File): string => {
  return URL.createObjectURL(file);
};

const removeFile = (index: number) => {
  selectedFiles.value.splice(index, 1);
};

const geocodeDireccion = async (direccion: string): Promise<{ lat: number; lon: number } | null> => {
  try {
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(direccion)}&format=json&limit=1`;
    
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'ReViews/1.0'
      }
    });
    
    if (!response.ok) {
      throw new Error('Error al geocodificar dirección');
    }
    
    const results = await response.json();
    
    if (results.length > 0) {
      return {
        lat: parseFloat(results[0].lat),
        lon: parseFloat(results[0].lon)
      };
    }
    
    return null;
  } catch (error) {
    console.error('Error en geocoding:', error);
    return null;
  }
};

const subirImagenes = async (): Promise<string[]> => {
  const urls: string[] = [];
  
  for (const file of selectedFiles.value) {
    try {
      const result = await resenaService.subirImagen(file);
      urls.push(result.url);
    } catch (error) {
      console.error('Error al subir imagen:', error);
      // Continuar con las demás imágenes
    }
  }
  
  return urls;
};

const guardarResena = async () => {
  if (!isFormValid.value) return;
  
  loading.value = true;
  errorMessage.value = '';
  
  try {
    // 1. Obtener coordenadas mediante geocoding
    const coords = await geocodeDireccion(formData.value.direccion);
    
    if (!coords) {
      errorMessage.value = 'No se pudieron obtener las coordenadas de la dirección. Verifica que sea correcta.';
      loading.value = false;
      return;
    }
    
    formData.value.latitud = coords.lat;
    formData.value.longitud = coords.lon;
    
    // 2. Subir imágenes si hay
    if (selectedFiles.value.length > 0) {
      const imageUrls = await subirImagenes();
      formData.value.imagenes = imageUrls;
    }
    
    // 3. Crear reseña (el backend añade automáticamente: email, nombre, token, fechas)
    await resenaService.crear(formData.value);
    
    // 4. Redirigir al home
    router.push('/');
  } catch (error: any) {
    console.error('Error al crear reseña:', error);
    errorMessage.value = error.message || 'Error al crear la reseña. Inténtalo de nuevo.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.form-container {
  padding: 16px;
  max-width: 800px;
  margin: 0 auto;
}

ion-item {
  --padding-start: 0;
  --inner-padding-end: 0;
  margin-bottom: 16px;
}

.rating-container {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0;
}

.star-clickable {
  cursor: pointer;
  transition: transform 0.2s;
}

.star-clickable:hover {
  transform: scale(1.2);
}

.rating-value {
  margin-left: 12px;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--ion-color-warning);
}

.images-preview {
  margin-top: 16px;
  padding: 16px;
  background: var(--ion-color-light);
  border-radius: 8px;
}

.preview-title {
  margin: 0 0 12px 0;
  font-weight: 600;
  color: var(--ion-color-medium);
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}

.preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid var(--ion-color-light-shade);
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  --background: rgba(255, 255, 255, 0.9);
  --border-radius: 50%;
  width: 32px;
  height: 32px;
  opacity: 0;
  transition: opacity 0.2s;
}

.preview-item:hover .remove-btn {
  opacity: 1;
}

.save-button {
  margin-top: 24px;
}

.error-message {
  margin-top: 16px;
  padding: 12px;
  background: var(--ion-color-danger-tint);
  border-radius: 8px;
}

.error-message p {
  margin: 0;
}
</style>
