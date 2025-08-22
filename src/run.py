from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Optional

# ---- SUMO tools einbinden
SUMO_HOME = os.environ.get("SUMO_HOME")
if not SUMO_HOME:
    raise RuntimeError("SUMO_HOME ist nicht gesetzt. Beispiel: $env:SUMO_HOME='C:\\Program Files (x86)\\Eclipse\\Sumo'")
TOOLS = Path(SUMO_HOME) / "tools"
sys.path.append(str(TOOLS))

import traci  # type: ignore
import sumolib  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
NET_DIR = ROOT / "net"
NET_FILE = NET_DIR / "rail.net.xml"
ROUTES_FILE = NET_DIR / "rail.routes.xml"
CFG_FILE = NET_DIR / "rail.sumocfg"


def _ensure_routes_from_net() -> None:
    """Erzeuge eine minimale rail.routes.xml aus rail.net.xml, falls sie fehlt."""
    if ROUTES_FILE.exists():
        return
    if not NET_FILE.exists():
        raise FileNotFoundError(f"Netz nicht gefunden: {NET_FILE}")

    net = sumolib.net.readNet(str(NET_FILE))

    # Wähle eine einfache Kette aus zwei verbundenen Kanten, die nicht "internal" sind.
    start_edge: Optional[sumolib.net.edge.Edge] = None
    next_edge: Optional[sumolib.net.edge.Edge] = None

    for e in net.getEdges():
        # interne/sonstige Hilfskanten überspringen
        if (e.getFunction() or "") in {"internal", "connector"}:
            continue
        outs = [o for o in e.getToNode().getOutgoing()
                if ((o.getFunction() or "") not in {"internal", "connector"})]
        if outs:
            start_edge = e
            next_edge = outs[0]
            break

    if not (start_edge and next_edge):
        raise RuntimeError("Konnte keine geeigneten Kantenpaare für eine Minimalroute finden.")

    edges_str = f"{start_edge.getID()} {next_edge.getID()}"

    ROUTES_FILE.write_text(
        f"""<routes>
  <vType id="train" vClass="rail" length="100" accel="0.5" decel="0.8" maxSpeed="27.78"/>
  <route id="r1" edges="{edges_str}"/>
  <vehicle id="t1" type="train" route="r1" depart="0"/>
</routes>
"""
        , encoding="utf-8"
    )


def _ensure_cfg() -> None:
    """Erzeuge rail.sumocfg falls fehlend."""
    if CFG_FILE.exists():
        return
    CFG_FILE.write_text(
        """<configuration>
  <input>
    <net-file value="rail.net.xml"/>
    <route-files value="rail.routes.xml"/>
  </input>
  <time>
    <begin value="0"/>
    <end value="200"/>
  </time>
  <report>
    <no-step-log value="true"/>
  </report>
</configuration>
"""
        , encoding="utf-8"
    )


def run(gui: bool = False, steps: int = 400) -> None:
    # Stelle sicher, dass wir alles zum Start haben
    _ensure_routes_from_net()
    _ensure_cfg()

    binary = "sumo-gui" if gui else "sumo"
    cmd = [binary, "-c", str(CFG_FILE), "--no-warnings", "true"]

    traci.start(cmd)
    try:
        for _ in range(steps):
            traci.simulationStep()
            if traci.simulation.getMinExpectedNumber() == 0:
                break
    finally:
        traci.close()


if __name__ == "__main__":
    gui = os.environ.get("SUMO_GUI", "0") == "1"
    run(gui=gui, steps=400)
