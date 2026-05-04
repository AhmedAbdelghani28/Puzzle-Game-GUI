#!/usr/bin/env bash
set -euo pipefail

DISPLAY_NUM=99
DISPLAY=:${DISPLAY_NUM}
VNC_PORT=5900
NOVNC_PORT=6080
RESOLUTION="1280x800x24"

# ── 1. Virtual framebuffer ─────────────────────────────────────────────────────
echo "[entrypoint] Starting Xvfb on display ${DISPLAY} (${RESOLUTION})"
Xvfb "${DISPLAY}" -screen 0 "${RESOLUTION}" -nolisten tcp &
XVFB_PID=$!

# Wait until Xvfb is accepting connections (xdpyinfo is installed via x11-utils)
for i in $(seq 1 30); do
    xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1 && break
    sleep 0.3
done
# Ensure Xvfb is up even if xdpyinfo check was inconclusive
sleep 0.5

# ── 2. VNC server ──────────────────────────────────────────────────────────────
echo "[entrypoint] Starting x11vnc on port ${VNC_PORT}"
x11vnc \
    -display "${DISPLAY}" \
    -rfbport "${VNC_PORT}" \
    -nopw \
    -listen localhost \
    -forever \
    -shared \
    -quiet \
    -bg   # daemonise

# ── 3. noVNC web proxy ─────────────────────────────────────────────────────────
echo "[entrypoint] Starting noVNC on port ${NOVNC_PORT}"
websockify \
    --web=/usr/share/novnc/ \
    --wrap-mode=ignore \
    "${NOVNC_PORT}" \
    "localhost:${VNC_PORT}" &

# ── 4. Launch the application ──────────────────────────────────────────────────
echo ""
echo "  ┌─────────────────────────────────────────────────┐"
echo "  │  Open in your browser:                          │"
echo "  │  http://localhost:${NOVNC_PORT}/vnc.html                │"
echo "  └─────────────────────────────────────────────────┘"
echo ""

export DISPLAY="${DISPLAY}"
exec python main.py
