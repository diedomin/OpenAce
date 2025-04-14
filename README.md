# OpenAce

**OpenAce** is an all-in-one Docker image. The proxy acts as an intermediary between an app and the AceStream engine or the IPTV server. The `/play/<content_id>` endpoint relays the MPEG-TS stream directly. It is useful for clients that support streaming, such as Jellyfin, Plex, etc. The `/hls/<content_id>` endpoint transforms that stream into HLS format (playlist `.m3u8` and `.ts` segments), allowing compatibility with players and servers such as Jellyfin, Plex, etc. The `/iptv/<seg1>/<seg2>/<seg3>` allows you to connect to your IPTV server over VPN, it can handle multiple IPTV servers in a single m3u list. All endpoints handle retries, errors, and logging for more robust content delivery.

> > Designed to integrate the AceStream engine and some IPTV services with servers such as Jellyfin or Plex.

---

## Features

- AceStream Engine + Proxy in a single container
- Optional VPN support (perfect with Gluetun)
- Automatic port forwarding support with some VPN providers such as Proton VPN (not all plans)
- Smart startup script that detects VPN mode or falls back to default settings
- Multiple IPTV servers in one list

---

## Getting Started

### Option 1: Simple (no VPN)

```bash
docker compose -f docker-compose_simple.yaml up -d
```

### Option 2: With VPN (Gluetun + WireGuard + Port Forwarding)

```bash
docker compose up -d
```

Make sure you provide the necessary Gluetun environment variables in an `.env` file.

For more information, please refer to [Gluetun VPN](https://github.com/qdm12/gluetun).

---

## Usage

- AceStream is exposed **internally** on port `6878`, but you can access the
  AceStream engine directly by exposing port 6878 of the container.
- The HTTP Proxy is exposed on port `8888` (defined in `docker-compose.yaml`)
- Use the proxy like this:

```
# For MPEG-TS streaming
http://<your-server>:8888/play/<acestream_content_id>

# For HLS streaming
http://<your-server>:8888/hls/<acestream_content_id>

# For IPTV streaming
http://<your-server>:8888/iptv/<seg1>/<seg2>/<seg3>
```

You can use this with servers such as Jellyfin via the "Live TV" function, simply by providing an `.m3u` file with the available streams, for example like this:

```
#EXTM3U

#EXTINF:-1 tvg-id="" tvg-name="NAME" group-title="Group",
http://<your-server>:8888/play/yourcontentid

#EXTINF:-1 tvg-id="" tvg-name="NAME" group-title="Group",
http://<your-server>:8888/hls/yoursecondcontentid

#EXTINF:-1 tvg-id="" tvg-name="NAME" group-title="Group",
http://<your-server>:8888/iptv/<seg1>/<seg2>/<seg3>
```

---

## How It Works

- On startup, `start.sh` checks if a Gluetun forwarded port is available.
- If detected, AceStream is launched using that port.
- The proxy starts with Gunicorn + Gevent to stream content via Flask.
- If no VPN is detected, it falls back to default port 6878.

---

## Build the image

```bash
docker build -t open-ace .
```

---

## Development tips

- You can use the image as-is.
- Or mount your own `start.sh` via volume to customize the startup behavior.
- Logs are printed via stdout and also written to log files, so `docker logs -f open-ace` works perfectly, as does `tail -f /your-path/proxy.log` or ingesting them into a log server like OpenSearch.

---

## Contributing

Got a cool idea? Found a bug?

1. Fork the repo
2. Create a feature branch
3. Open a PR — let's make streaming better together!

---

## License

MIT — use it freely, fork it, break it, improve it.

---

## Like this project?

Spread the word. Star the repo and share it with others!
