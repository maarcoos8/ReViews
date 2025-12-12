# Backend Dockerfile para ReViews
FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para aprovechar el caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app/ ./app/

# Exponer el puerto
EXPOSE 8000

# El comando se define en docker-compose.yml para permitir --reload en desarrollo
# Para producción: CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

