# Despliegue en Vercel - ReViews

## Configuración Previa

### 1. Variables de Entorno en Vercel
Debes configurar las siguientes variables de entorno en tu proyecto de Vercel:

```bash
MONGO_URL=mongodb+srv://usuario:password@cluster.mongodb.net/reviews?retryWrites=true&w=majority
JWT_SECRET_KEY=tu-clave-secreta-muy-segura-aqui
GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-google-client-secret
FRONTEND_URL=https://tu-dominio.vercel.app
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

### 2. Configurar MongoDB Atlas
1. Crea una cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crea un cluster gratuito
3. Configura Network Access para permitir conexiones desde Vercel (IP: `0.0.0.0/0`)
4. Crea un usuario de base de datos
5. Obtén la cadena de conexión y úsala como `MONGO_URL`

### 3. Configurar Google OAuth
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+
4. Crea credenciales OAuth 2.0
5. Agrega las URIs autorizadas:
   - JavaScript origins: `https://tu-dominio.vercel.app`
   - Redirect URIs: `https://tu-dominio.vercel.app/auth/callback`

### 4. Configurar Cloudinary
1. Crea una cuenta en [Cloudinary](https://cloudinary.com/)
2. Obtén tus credenciales del dashboard
3. Configúralas en las variables de entorno de Vercel

## Despliegue

### Opción 1: Desde el Dashboard de Vercel
1. Conecta tu repositorio de GitHub a Vercel
2. Selecciona el proyecto
3. Vercel detectará automáticamente el `vercel.json`
4. Configura las variables de entorno
5. Despliega

### Opción 2: Usando Vercel CLI
```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Desplegar (primera vez)
vercel

# Desplegar a producción
vercel --prod
```

## Estructura del Proyecto

```
ReViews/
├── api/
│   └── index.py          # Entry point para Vercel Serverless
├── backend/
│   └── app/
│       ├── main.py       # FastAPI app principal
│       ├── routers/      # Rutas de la API
│       ├── models/       # Modelos de MongoDB
│       └── ...
├── frontend/
│   ├── src/              # Código fuente Vue
│   ├── dist/             # Build de producción (generado)
│   └── package.json
├── vercel.json           # Configuración de Vercel
├── requirements.txt      # Dependencias Python
└── .vercelignore         # Archivos a ignorar en deploy

```

## Notas Importantes

1. **CORS**: El backend ya está configurado para aceptar peticiones del frontend en `main.py`
2. **Root Path**: FastAPI usa `root_path="/api"` para funcionar correctamente con Vercel
3. **Serverless**: El backend se ejecuta como función serverless, compatible con cold starts
4. **Frontend**: Se construye con `npm run build` y se sirve como sitio estático
5. **Database**: MongoDB Atlas es necesario (no se puede usar MongoDB local)

## Verificación Post-Despliegue

1. Verifica que el frontend carga: `https://tu-dominio.vercel.app`
2. Verifica que la API funciona: `https://tu-dominio.vercel.app/api/docs`
3. Prueba el login con Google OAuth
4. Crea una reseña de prueba

## Troubleshooting

### Error 500 en /api
- Verifica que todas las variables de entorno estén configuradas
- Revisa los logs en el dashboard de Vercel
- Asegúrate de que MongoDB Atlas permita conexiones desde Vercel

### OAuth no funciona
- Verifica las URIs de redirección en Google Cloud Console
- Asegúrate de que `FRONTEND_URL` sea correcto
- Revisa que `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` sean correctos

### Frontend no carga
- Ejecuta `npm run build` localmente para verificar que compila
- Revisa la configuración de `vite.config.ts`
- Verifica que `frontend/dist` se esté generando correctamente
