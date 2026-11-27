# ReticulumBridge

Dies verbindet die Welten des Reticulums mit den anderen Programmen. Es werden die erhaltenen Daten in die InfluxDB geschrieben und teils per REST API zur verfügung gestellt. Dazu kann über die REST API Steuerbefehle via Reticulum senden.

## Anforderung

- die Brige kann via config.yml konfiguriert werden (bsp. Reticulum Identiy)
- die Brige bietet eine REST API an und nutzt dafür FastAPI
- die Brige schreibt ausgewählte daten in die Influx DB

Für lokale Tests kann `reticulum_bridge.use_dummy_bridge` in `config.yml`
auf `true` gesetzt werden. Dann erzeugt die Dummy-Bridge zu jedem Befehl eine
erfolgreiche Antwort und leitet sie über den Reticulum-Router weiter. Bei
`false` wird die echte Reticulum-Bridge verwendet; `false` ist auch der
Standardwert im Settings-Modell.

## Reticulum-Nachrichtenformat

Nachrichten werden als JSON-Envelope mit einem `type`-Feld und den Modelldaten
im Feld `data` übertragen. Unterstützte Typen sind `command`, `response` und
`telemetry`. Das `type`-Feld ist nötig, weil `CommandData` und `ResponseData`
aktuell dieselbe Feldstruktur haben.

```json
{"type": "command", "data": {"timestamp": "2025-01-01T00:00:00Z", "id": 42}}
```

Die Live-Demo sendet regelmäßig Telemetrie sowie die Befehle `ping`,
`get_status` und `set_mode`. Die Demo-Gegenstelle beantwortet jeden Befehl;
`receiveMsg` verarbeitet ausschließlich diese Antworten.

HTTP-Anfragen werden mit Methode, Pfad, Statuscode und Laufzeit protokolliert.
Fehlerantworten ab Statuscode 400 werden als Warnung geloggt; Antwortinhalte
und Header werden zum Schutz sensibler Daten nicht mitgeschrieben.

### How to run dev env

docker compose up -d influxdb grafana dozzle
