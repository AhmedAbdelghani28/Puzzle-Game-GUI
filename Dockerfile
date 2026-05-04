# ── Build stage: install Python deps ──────────────────────────────────────────
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    # Force Qt to use the XCB (X11) backend inside the container
    QT_QPA_PLATFORM=xcb \
    DISPLAY=:99 \
    # Suppress Qt font warnings in a headless environment
    QT_LOGGING_RULES="*.debug=false;qt.qpa.*=false"

# System packages:
#   xvfb         – virtual framebuffer (the "fake screen")
#   x11vnc       – VNC server that streams the framebuffer
#   novnc        – browser-based VNC viewer (HTML5 / WebSockets)
#   websockify   – WebSocket proxy that connects noVNC to x11vnc
#   libxcb-*     – XCB runtime libraries required by Qt6/Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
        xvfb \
        x11vnc \
        novnc \
        websockify \
        libgl1 \
        libglib2.0-0 \
        libdbus-1-3 \
        libxcb1 \
        libx11-xcb1 \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libxkbcommon-x11-0 \
        libxi6 \
        libxrender1 \
        libxrandr2 \
        libxfixes3 \
        libegl1 \
        libfontconfig1 \
        libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-built Python packages from builder stage
COPY --from=builder /install /usr/local

WORKDIR /app
COPY . .

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# noVNC web UI
EXPOSE 6080

ENTRYPOINT ["/entrypoint.sh"]
