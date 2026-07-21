FROM python:3.12-slim

WORKDIR /app

# Instalar Tkinter y herramientas de compilación para dependencias de Python (como chromadb)
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Ejecutar la aplicación
CMD ["sh", "-c", "streamlit run iespro_taller/services/app_web.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]