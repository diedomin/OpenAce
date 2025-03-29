#!/bin/bash
set -e

# Start cron daemon
cron

FORWARDED_PORT_FILE="/tmp/gluetun/forwarded_port"

# Wait until the file exists and has content (max 20 seconds)
echo "🔍 Looking for Gluetun port file: $FORWARDED_PORT_FILE"
for i in {1..20}; do
  if [[ -s "$FORWARDED_PORT_FILE" ]]; then
    PORT=$(cat "$FORWARDED_PORT_FILE")
    echo "Port successfully retrieved from Gluetun: $PORT"
    break
  fi
  echo "Gluetun hasn't provided a port yet, waiting... ($i/20)"
  sleep 1
done

# If no forwarded port, use default
if [[ -z "$PORT" ]]; then
  PORT=${ACESTREAM_PORT:-6878}
  echo "No forwarded port found, falling back to default: $PORT"
fi

# Start AceStream engine in the background
echo "Starting AceStream on port $PORT..."
/app/start-engine --client-console --port "$PORT" >> /var/log/openace/acestream.log 2>&1 &

# Start proxy in the foreground
exec gunicorn --worker-class gevent --bind 0.0.0.0:8888 --timeout 3600 server:app
