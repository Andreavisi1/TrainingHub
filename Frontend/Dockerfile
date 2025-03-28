# Usa l'immagine ufficiale Python come base
FROM python:3.10

# Imposta la directory di lavoro
WORKDIR /app

# Imposta variabili d'ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il progetto
COPY . .

# Crea la directory per i file caricati e imposta i permessi
RUN mkdir -p uploads && chmod 777 uploads

# Esponi la porta su cui l'app sarà in ascolto
EXPOSE 5000

# Comando per avviare l'applicazione
CMD ["python", "app.py"]