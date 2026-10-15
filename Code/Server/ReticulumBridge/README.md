# ReticulumBridge

Dies verbindet die Welten des Reticulums mit den anderen Programmen. Es werden die erhaltenen Daten in die InfluxDB geschrieben und teils per REST API zur verfügung gestellt. Dazu kann über die REST API Steuerbefehle via Reticulum senden.

## Anforderung

- die Brige kann via config.yml konfiguriert werden (bsp. Reticulum Identiy)
- die Brige bietet eine REST API an und nutzt dafür FastAPI
- die Brige schreibt ausgewählte daten in die Influx DB

