#!/bin/bash

echo "📦 Systempakete aktualisieren..."
sudo apt update && sudo apt install -y python3-pip git

echo "✅ Prüfen, ob pip installiert ist..."
pip3 --version || { echo "❌ pip3 konnte nicht installiert werden."; exit 1; }

echo "📁 Projektverzeichnis prüfen..."
if [ ! -d "digitales-KVP-Tool" ]; then
  echo "⬇️ Projekt wird von GitHub geklont..."
  git clone https://github.com/toukoalvine/digitales-KVP-Tool.git
fi

cd digitales-KVP-Tool || { echo "❌ Projektverzeichnis nicht gefunden."; exit 1; }

echo "📦 Streamlit installieren (lokal für den Benutzer)..."
pip3 install --user streamlit

echo "🚀 Starte Streamlit-App..."
~/.local/bin/streamlit run streamlit_app.py \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --server.port 8501 \
  --server.address 0.0.0.0
