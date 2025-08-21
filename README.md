Vorschlag README.md
# SUMO Proof of Concept (Bachelor Thesis)

Dieses Repository enthält einen minimalen Proof of Concept (PoC) für die Nutzung von [SUMO – Simulation of Urban MObility](https://www.eclipse.org/sumo/) im Rahmen der Bachelorarbeit **Kapazitätsmanagement im regionalen Schienenverkehr**.

Ziel: Eine lauffähige Beispielsimulation (kleines Grid-Netzwerk mit zufälligen Fahrzeugen) sowie ein Python-Skript zur Steuerung der Simulation über **TraCI**.

---

## Projektstruktur



01_poc/
├─ net/ # Netz- und Routen-Dateien (XML)
│ ├─ simple.net.xml # generiertes Netz (2x2 Grid)
│ ├─ simple.rou.xml # generierte Routen (via randomTrips.py)
│ └─ simple.sumocfg # Simulation Config
├─ src/
│ └─ run.py # Python PoC mit TraCI
├─ tests/
│ └─ test_env.py # Smoke-Tests (pytest)
├─ requirements.txt # Python Dependencies
├─ .gitignore
└─ README.md


---

## Setup

### 1. Voraussetzungen
- Python ≥ 3.11
- SUMO (installiert via Wizard oder Paket)
- Git

### 2. Environment
```powershell
cd 01_poc
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

3. Umgebungsvariablen

In PowerShell (temporär):

$env:SUMO_HOME = "C:\Program Files\Eclipse\Sumo"
$env:Path = "$env:SUMO_HOME\bin;$env:Path"

4. Netz und Routen generieren
cd net
netgenerate --grid --grid.number=2 --output-file=simple.net.xml
python "$env:SUMO_HOME\tools\randomTrips.py" -n simple.net.xml -o simple.rou.xml -e 300 --seed 42 --validate

5. Simulation starten

GUI:

sumo-gui -c simple.sumocfg


Headless:

sumo -c simple.sumocfg

Python PoC mit TraCI
cd src
python run.py


Ausgabe (Beispiel):

Step 0: 1 Fahrzeuge aktiv: ['veh0']
Step 1: 2 Fahrzeuge aktiv: ['veh0', 'veh1']
...

Tests
pytest tests

Nächste Schritte

Eigene Netzwerke erstellen (z. B. Engstellen-Szenarien)

Reward-Shaping und Metriken (Travel Time, Waiting Time, Durchsatz)

Integration in DRL-Frameworks (PPO/DQN)

Vergleichbare Setup-Logik wie in Flatland (Smoke → Dev → Stress Szenarien)