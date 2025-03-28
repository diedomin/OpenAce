# 🎬 OpenAce

**OpenAce** is a lightweight, all-in-one Docker image that bundles the AceStream engine and a modern HTTP proxy to easily stream content over HTTP — with or without a VPN.

> 🔧 > Designed to integrate Acestream engine over servers such as Jellyfin or Plex.

---

## 🌐 Features

- ✅ AceStream Engine + Proxy in one single container
- 🔄 Optional WireGuard VPN support (perfect with Gluetun)
- 🚪 Automatic port forwarding support with some VPN providers such as Proton VPN (not all plans)
- 🧠 Smart startup script to detect VPN mode or fallback

---

## 🚀 Getting Started

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

## 🧾 Folder structure

```
open-ace/
├── Dockerfile               # Builds the full image
├── docker-compose.yaml      # VPN + Port Forwarding setup
├── docker-compose_simple.yaml # Simple setup (no VPN)
├── server.py                # Flask proxy for AceStream
├── start.sh                 # Smart entrypoint script
├── README.md                # You're reading it
└── .env                     # Secrets and WireGuard config (not included)
```

---

## 📡 Usage

- AceStream is exposed **internally** on port `6878`
- The HTTP Proxy is exposed on port `8888` (defined in `docker-compose.yaml`)
- Use the proxy like this:

```
http://<your-server>:8888/play/<acestream_content_id>
```

---

## 🧠 How It Works

- On startup, `start.sh` checks if a Gluetun forwarded port is available.
- If detected, AceStream is launched using that port.
- The proxy starts with Gunicorn + Gevent to stream content via Flask.
- If no VPN is detected, it falls back to default port 6878.

---

## 📦 Build the image

```bash
docker build -t open-ace .
```

---

## 🛠 Development tips

- You can use the image as-is.
- Or mount your own `start.sh` via volume to customize the startup behavior.
- Logs are printed via stdout, so `docker logs -f open-ace` works perfectly.

---

## 🤝 Contributing

Got a cool idea? Found a bug?

1. Fork the repo
2. Create a feature branch
3. Open a PR — let's make streaming better together!

---

## 🪪 License

MIT — use it freely, fork it, break it, improve it.

---

## ⭐️ Like this project?

Spread the word. Star the repo.
