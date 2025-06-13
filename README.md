# digitales-KVP-Tool
# 🔄 Digitales KVP-Tool

Ein umfassendes **Kontinuierlicher Verbesserungsprozess (KVP)** Tool basierend auf dem **PDCA-Zyklus** (Plan-Do-Check-Act), entwickelt mit Streamlit.

## 📋 Inhaltsverzeichnis

- [Features](#-features)
- [Installation](#-installation)
- [Schnellstart](#-schnellstart)
- [Benutzeranleitung](#-benutzeranleitung)
- [PDCA-Phasen](#-pdca-phasen)
- [Benutzerrollen](#-benutzerrollen)
- [Screenshots](#-screenshots)
- [Technische Details](#-technische-details)
- [Erweiterungen](#-erweiterungen)
- [Troubleshooting](#-troubleshooting)
- [Beitragen](#-beitragen)
- [Lizenz](#-lizenz)

## ✨ Features

### 🎯 Kernfunktionen
- **PDCA-Zyklus Navigation**: Strukturierte Führung durch alle vier Phasen
- **Projekt-Management**: Erstellen, bearbeiten und verwalten mehrerer KVP-Projekte
- **Aufgaben-Tracking**: To-do-Listen mit Zuständigkeiten, Fälligkeiten und Status
- **Fortschritts-Visualisierung**: Echtzeit-Dashboards und Kennzahlen
- **Auto-Speicherung**: Keine manuellen Speichervorgänge erforderlich

### 📊 Visualisierung & Reporting
- **Interactive Dashboards**: KPIs, Fortschrittsanzeigen und Metriken
- **Diagramme**: Pie-Charts, Bar-Charts und Trend-Analysen
- **Export-Funktionen**: JSON-Export für Datensicherung und -austausch
- **Druckfreundliche Ansichten**: Optimiert für Berichte und Präsentationen

### 👥 Teamwork & Rollen
- **Benutzerrollen**: Admin, Bearbeiter, Leser mit entsprechenden Berechtigungen
- **Zuständigkeiten**: Klare Aufgabenverteilung im Team
- **Collaborative Features**: Kommentar-System (erweiterbar)

### 🔧 Benutzerfreundlichkeit
- **Onboarding**: Integrierte Tool-Tour und Hilfe-System
- **Beispielprojekt**: Vorgefertigte Daten zum Ausprobieren
- **Responsive Design**: Funktioniert auf Desktop und Tablet
- **Tooltips**: Kontextuelle Hilfe bei allen Eingabefeldern

## 🚀 Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### 1. Repository klonen
```bash
git clone https://github.com/ihr-username/kvp-tool.git
cd kvp-tool
```

### 2. Virtuelle Umgebung erstellen (empfohlen)
```bash
python -m venv kvp-env
source kvp-env/bin/activate  # Linux/Mac
# oder
kvp-env\Scripts\activate     # Windows
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Schnellstart

### 1. Anwendung starten
```bash
streamlit run kvp_tool.py
```

### 2. Browser öffnen
Die Anwendung öffnet sich automatisch unter: `http://localhost:8501`

### 3. Erstes Projekt erstellen
1. Klicken Sie auf "📝 Beispielprojekt laden" für eine Demo
2. Oder erstellen Sie ein "➕ Neues Projekt"
3. Arbeiten Sie sich durch die PDCA-Phasen

## 📖 Benutzeranleitung

### Projekt erstellen
1. **Sidebar**: Klicken Sie auf "➕ Neues Projekt"
2. **Projektname**: Geben Sie einen aussagekräftigen Namen ein
3. **Status**: Wählen Sie den aktuellen Projektstatus
4. **Beschreibung**: Fügen Sie eine kurze Projektbeschreibung hinzu

### Navigation
- **Tabs**: Verwenden Sie die Tabs für PDCA-Phasen und Dashboard
- **Sidebar**: Projektauswahl und Benutzerrolle
- **Fortschrittsleiste**: Zeigt den aktuellen PDCA-Fortschritt

### Daten exportieren
1. **Sidebar**: Klicken Sie auf "📥 Projekt exportieren"
2. **Download**: JSON-Datei mit allen Projektdaten
3. **Import**: JSON-Dateien können später wieder importiert werden (Feature in Entwicklung)

## 🔄 PDCA-Phasen

### 📋 Plan (Planen)
- **Problemdefinition**: Konkrete Beschreibung des zu lösenden Problems
- **Zielsetzung**: SMART-Ziele (Spezifisch, Messbar, Erreichbar, Relevant, Terminiert)
- **Ursachenanalyse**: Root-Cause-Analyse mit bewährten Methoden
- **Maßnahmenplanung**: Detaillierte Aktionspläne

### 🔨 Do (Umsetzen)
- **Aufgaben-Management**: Erstellen und verwalten von To-dos
- **Zuständigkeiten**: Klare Verantwortlichkeiten definieren
- **Terminplanung**: Fälligkeitsdaten und Meilensteine
- **Status-Tracking**: Fortschritt in Echtzeit verfolgen

### 📊 Check (Überprüfen)
- **Kennzahlen**: Vorher-Nachher-Vergleiche
- **Ergebnisbewertung**: Qualitative und quantitative Analyse
- **Abweichungsanalyse**: Soll-Ist-Vergleiche
- **Visualisierung**: Grafische Darstellung der Ergebnisse

### 🎯 Act (Handeln)
- **Standardisierung**: Dauerhafte Verankerung von Verbesserungen
- **Lessons Learned**: Erkenntnisse für zukünftige Projekte
- **Nächste Schritte**: Folgemaßnahmen und Ausweitung
- **Dokumentation**: Wissensmanagement und Best Practices

## 👥 Benutzerrollen

### 🔑 Admin
- Vollzugriff auf alle Funktionen
- Projekte erstellen, bearbeiten und löschen
- Benutzerrollen verwalten
- Export- und Backup-Funktionen

### ✏️ Bearbeiter
- Projekte bearbeiten und aktualisieren
- Aufgaben erstellen und verwalten
- Kommentare hinzufügen
- Daten eingeben und Status ändern

### 👁️ Leser
- Projekte und Dashboards anzeigen
- Berichte und Visualisierungen betrachten
- Export-Funktionen (nur Lesen)
- Keine Bearbeitungsrechte

## 📸 Screenshots

### Dashboard
- Übersichtliche KPIs und Metriken
- Interaktive Diagramme
- Fortschrittsanzeigen
- Status-Visualisierungen

### PDCA-Navigation
- Farbkodierte Phasen
- Fortschrittsleiste
- Intuitive Tab-Navigation
- Kontextuelle Hilfe

## 🔧 Technische Details

### Architektur
```
kvp-tool/
├── kvp_tool.py          # Hauptanwendung
├── requirements.txt     # Python-Abhängigkeiten
├── README.md           # Diese Datei
├── data/               # Datenverzeichnis (optional)
├── exports/            # Export-Verzeichnis (optional)
└── docs/               # Dokumentation (optional)
```

### Technologie-Stack
- **Frontend**: Streamlit (Python Web Framework)
- **Visualisierung**: Plotly für interaktive Diagramme
- **Datenverarbeitung**: Pandas für Datenmanipulation
- **Storage**: JSON-basiert (erweiterbar zu SQLite/PostgreSQL)

### Performance
- **Startup-Zeit**: < 3 Sekunden
- **Responsive Design**: Optimiert für Desktop und Tablet
- **Browser-Kompatibilität**: Chrome, Firefox, Safari, Edge

## 🚧 Erweiterungen

### Geplante Features
- [ ] **Datenbank-Integration**: SQLite/PostgreSQL Backend
- [ ] **Authentifizierung**: Multi-User-System mit Login
- [ ] **E-Mail-Benachrichtigungen**: Automatische Erinnerungen
- [ ] **PDF-Export**: Professionelle Berichte
- [ ] **File-Upload**: Dokumente und Bilder
- [ ] **Gantt-Charts**: Erweiterte Zeitplanung
- [ ] **API-Integration**: REST-API für externe Systeme

### Einfache Erweiterungen
```python
# Beispiel: Neue Kennzahl hinzufügen
def add_custom_metric(project_data, metric_name, value):
    if 'custom_metrics' not in project_data['check']:
        project_data['check']['custom_metrics'] = {}
    project_data['check']['custom_metrics'][metric_name] = value
```

## 🐛 Troubleshooting

### Häufige Probleme

#### Anwendung startet nicht
```bash
# Überprüfen Sie die Python-Version
python --version

# Abhängigkeiten neu installieren
pip install -r requirements.txt --upgrade

# Streamlit Version prüfen
streamlit version
```

#### Browser öffnet sich nicht automatisch
```bash
# Manuelle URL öffnen
# http://localhost:8501
```

#### Daten gehen verloren
- **Problem**: Session State wird bei Neustart gelöscht
- **Lösung**: Verwenden Sie die Export-Funktion regelmäßig
- **Zukunft**: Persistente Datenbankanbindung geplant

#### Performance-Probleme
- **Große Projekte**: Verwenden Sie mehrere kleinere Projekte
- **Browser-Cache**: Leeren Sie den Browser-Cache
- **System-Ressourcen**: Schließen Sie nicht verwendete Browser-Tabs

### Log-Ausgaben
```bash
# Detaillierte Logs aktivieren
streamlit run kvp_tool.py --logger.level=debug
```

## 🤝 Beitragen

Wir freuen uns über Beiträge! Hier ist wie Sie mitmachen können:

### 1. Fork des Repositories
```bash
git fork https://github.com/ihr-username/kvp-tool.git
```

### 2. Feature-Branch erstellen
```bash
git checkout -b feature/neue-funktionalität
```

### 3. Änderungen committen
```bash
git commit -m "Füge neue Funktionalität hinzu"
```

### 4. Pull Request erstellen
- Beschreibung der Änderungen
- Screenshots bei UI-Änderungen
- Tests für neue Features

### Code-Standards
- **PEP 8**: Python-Stil-Guide befolgen
- **Dokumentation**: Docstrings für alle Funktionen
- **Kommentare**: Komplexe Logik erklären
- **Testing**: Unit-Tests für kritische Funktionen

## 📄 Lizenz

###

## 📞 Support

- **Issues**: https://github.com/toukoalvine/digitales-KVP-Tool
- **E-Mail**: toukoalvine@yahoo.fr

## 🙏 Danksagungen

- **Streamlit Team**: Für das großartige Framework
- **Plotly**: Für die interaktiven Visualisierungen
- **KVP-Community**: Für Feedback und Ideen
---
**Entwickelt mit ❤️ für kontinuierliche Verbesserung**
*Letzte Aktualisierung: Juni 2025*
