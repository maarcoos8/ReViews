# AGENTS.md - Protocolo de Actuación para Agentes de Código

Este archivo define el protocolo estricto que debes seguir como Agente de IA al trabajar en este repositorio.

## 1. Fase de Análisis de Contexto
Antes de generar cualquier línea de código o respuesta, **DEBES** leer y comprender los prompts específicos de la tecnología involucrada:

- Si la tarea implica **Backend**, lee `gemini/backend/BACKEND_PROMPT.md` (o la referencia proporcionada en el prompt del sistema).
- Si la tarea implica **Frontend**, lee `gemini/frontend/FRONTEND_PROMPT.md`.
- Si es **Fullstack**, integra las directrices de ambos.

## 2. Método de Trabajo (Workflow)
El usuario espera una ejecución precisa y alineada con la arquitectura existente.

1. **Identificar la Capa:** Determina si el cambio afecta a Modelos (DB), API (Backend), Estado (Frontend) o UI.
2. **Revisar Dependencias:**
   - En Backend: ¿Afecta a `requirements.txt` o `docker-compose.yml`?
   - En Frontend: ¿Requiere nuevos paquetes en `package.json` o configuración en `vite.config.ts`?
3. **Consistencia de Estilo:**
   - Backend: Usa Pydantic v2, Beanie y Async/Await. Respeta la estructura `routers/` vs `crud/`.
   - Frontend: Usa Vue 3 Composition API y componentes Ionic. Mantén la lógica en `services` y `stores`.
4. **Verificación:** Antes de dar la solución final, simula mentalmente si el código compilaría con las configuraciones actuales (ej. imports de Leaflet, conexión a Mongo).

## 3. Restricciones Críticas
- **NO** introduzcas librerías nuevas sin justificación crítica.
- **NO** cambies la arquitectura de carpetas (ej. no muevas la lógica de `crud` a `routers`).
- **NO** mezcles lógica síncrona en endpoints asíncronos de FastAPI.
- Respeta siempre el principio de "Mobile First" en el frontend dado el uso de Ionic/Capacitor.

## 4. Objetivo
Tu objetivo es actuar como un desarrollador senior que conoce el proyecto desde el día 1. No expliques conceptos básicos, ve al grano y proporciona código que se integre sin fricción en los archivos existentes.