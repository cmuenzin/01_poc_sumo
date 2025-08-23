# SUMO Proof of Concept (Bachelor Thesis)

Dieses Repository enthält einen minimalen Proof of Concept (PoC) für die Nutzung von [SUMO – Simulation of Urban MObility](https://www.eclipse.org/sumo/) im Rahmen der Bachelorarbeit **Kapazitätsmanagement im regionalen Schienenverkehr**.

**Ziel:** Eine lauffähige Beispielsimulation (kleines Grid-Netzwerk mit zufälligen Fahrzeugen) sowie ein Python-Skript zur Steuerung der Simulation über **TraCI**.

---

## Projektstruktur

```
├── src/
│   └── run.py              # Python PoC mit TraCI
├── tests/
│   └── test_env.py         # Smoke-Tests (pytest)
├── .gitignore              # Git ignore rules
└── README.md               # Diese Datei
```

**Hinweis:** Netz- und Routen-Dateien (XML) werden zur Laufzeit generiert und sind in der `.gitignore` ausgeschlossen.

---

## Setup

### 1. Voraussetzungen
- Python ≥ 3.11
- SUMO (installiert via Wizard oder Paket)
- Git

### 2. Environment Setup
```powershell
# Repository klonen und Virtual Environment erstellen
git clone <repository-url>
cd 01_poc_sumo
python -m venv .venv
.venv\Scripts\activate

# Dependencies installieren (falls requirements.txt vorhanden)
pip install sumo pytest
```

### 3. Umgebungsvariablen
In PowerShell (temporär):
```powershell
$env:SUMO_HOME = "C:\Program Files\Eclipse\Sumo"
$env:Path = "$env:SUMO_HOME\bin;$env:Path"
```

### 4. Netz und Routen generieren
```powershell
# Verzeichnis für Netz-Dateien erstellen
mkdir net
cd net

# Grid-Netzwerk generieren
netgenerate --grid --grid.number=2 --output-file=simple.net.xml

# Zufällige Routen generieren
python "$env:SUMO_HOME\tools\randomTrips.py" -n simple.net.xml -o simple.rou.xml -e 300 --seed 42 --validate
```

### 5. Simulation starten

**GUI Version:**
```powershell
sumo-gui -c simple.sumocfg
```

**Headless Version:**
```powershell
sumo -c simple.sumocfg
```

**Python PoC mit TraCI:**
```powershell
cd src
python run.py
```

---

**Beispiel-Ausgabe:**

```
Step 0: 1 Fahrzeuge aktiv: ['veh0']
Step 1: 2 Fahrzeuge aktiv: ['veh0', 'veh1']
...
```

## Tests

Tests ausführen:
```bash
pytest tests
```

---

## Nächste Schritte

- **Eigene Netzwerke erstellen** (z. B. Engstellen-Szenarien)
- **Reward-Shaping und Metriken** (Travel Time, Waiting Time, Durchsatz)
- **Integration in DRL-Frameworks** (PPO/DQN)
- **Vergleichbare Setup-Logik wie in Flatland** (Smoke → Dev → Stress Szenarien)