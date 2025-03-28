FROM python:3.10-slim

WORKDIR /app

# Installa le dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copia i file necessari
COPY requirements.txt .
COPY skills_extractor.py .

# Installa le dipendenze Python con supporto CUDA
RUN pip install --no-cache-dir -r requirements.txt

# Crea directory per i modelli e gli output
RUN mkdir -p /app/models /app/input /app/output

# Imposta le variabili d'ambiente
ENV MODEL_PATH=/app/models/Meta-Llama-3-8B-Instruct.Q2_K.gguf

# Script di entrypoint
ENTRYPOINT ["python", "skills_extractor.py"]

# Comando predefinito (può essere sovrascritto)
CMD ["--help"]