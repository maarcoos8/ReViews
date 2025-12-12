"""
Entry point para Vercel Serverless Functions
Este archivo adapta la aplicación FastAPI para funcionar como una función serverless en Vercel
"""
import sys
from pathlib import Path

# Agregar el directorio backend al path para imports
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.main import app

# Vercel espera que la app esté disponible como variable global
# FastAPI ya es compatible con ASGI, por lo que Vercel puede usarlo directamente
