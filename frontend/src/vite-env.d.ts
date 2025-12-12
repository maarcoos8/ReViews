/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  // Añade más variables de entorno aquí si es necesario
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
