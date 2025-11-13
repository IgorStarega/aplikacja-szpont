# Docker Support dla Aktualizator Strony v5.2
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & python apk.py"]
# Uruchom X virtual framebuffer dla GUI

EXPOSE 8080
# Port dla API (v5.1+)

EXPOSE 5000
# Port dla Web Dashboard (v5.1+)

RUN chmod +x apk.py
# Ustaw uprawnienia

RUN mkdir -p logs backups src/.data src/.cache src/.config config
# Utwórz katalogi

COPY . .
# Skopiuj aplikację

RUN pip install --no-cache-dir -r requirements.txt
# Zainstaluj zależności Python

COPY requirements.txt .
# Skopiuj pliki wymagań

WORKDIR /app
# Ustaw katalog roboczy

    && rm -rf /var/lib/apt/lists/*
    libgomp1 \
    libxrender-dev \
    libxext6 \
    libsm6 \
    libglib2.0-0 \
    fluxbox \
    x11vnc \
    xvfb \
    git \
RUN apt-get update && apt-get install -y \
# Zainstaluj zależności systemowe

ENV DISPLAY=:99
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Ustaw zmienne środowiskowe

FROM python:3.11-slim


