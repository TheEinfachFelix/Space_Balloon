# Offizielles Python-Image mit vorinstalliertem uv
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Performance-Optimierungen für uv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# 1. Zuerst nur die Projekt-Metadaten und die Lockfile kopieren
COPY pyproject.toml uv.lock .python-version README.md ./

# 2. Abhängigkeiten installieren (ohne den eigentlichen src-Code),
# damit dieser Schritt im Docker-Cache bleibt, wenn du später Code änderst.
RUN uv sync --frozen --no-dev --no-install-project

# 3. Erst jetzt den eigentlichen Quellcode kopieren
COPY src/ ./src/

# 4. Das Projekt selbst in die virtuelle Umgebung installieren
RUN uv sync --frozen --no-dev

# 5. Startbefehl: Führt dein Modul direkt über die von uv erstellte virtuelle Umgebung aus
CMD ["/app/.venv/bin/cellcon"]
