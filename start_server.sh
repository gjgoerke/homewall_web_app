#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DJANGO_DIR="$SCRIPT_DIR/homewall_django"

cd "$DJANGO_DIR"

if [[ -f "$DJANGO_DIR/venv/bin/activate" ]]; then
  source "$DJANGO_DIR/venv/bin/activate"
elif [[ -f "$SCRIPT_DIR/homewall/bin/activate" ]]; then
  source "$SCRIPT_DIR/homewall/bin/activate"
else
  echo "No virtual environment found."
  echo ""
  echo "Create one with:"
  echo "  cd \"$DJANGO_DIR\""
  echo "  python3 -m venv venv"
  echo "  source venv/bin/activate"
  echo "  pip install django==5.1.1 djangorestframework==3.15.2"
  exit 1
fi

IP="$(ipconfig getifaddr en0 2>/dev/null || true)"
if [[ -z "$IP" ]]; then
  IP="$(ipconfig getifaddr en1 2>/dev/null || true)"
fi

echo ""
echo "Homewall server starting..."
echo ""
echo "  On this Mac:  http://localhost:8000"
if [[ -n "$IP" ]]; then
  echo "  On your phone: http://${IP}:8000"
else
  echo "  Could not detect Wi-Fi IP — check System Settings → Network"
fi
echo ""
echo "Press Ctrl+C to stop."
echo ""

python manage.py runserver 0.0.0.0:8000
