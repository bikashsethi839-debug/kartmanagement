#!/usr/bin/env bash
set -euo pipefail

CERT_DIR=certs
CERT_KEY="$CERT_DIR/dev.key"
CERT_CRT="$CERT_DIR/dev.crt"
mkdir -p "$CERT_DIR"

if [ ! -f "$CERT_KEY" ] || [ ! -f "$CERT_CRT" ]; then
  echo "Generating self-signed certificate for development in $CERT_DIR"
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/CN=localhost" -keyout "$CERT_KEY" -out "$CERT_CRT"
fi

echo "Starting Python built-in HTTP server (plain HTTP)..."
exec python /workspaces/kartmanagement/app.py --no-https
