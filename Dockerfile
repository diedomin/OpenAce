FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# 🔧 System dependencies
RUN apt update && apt install -y --no-install-recommends \
    wget curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# ⬇️ Download and extract AceStream Engine
RUN wget -q "https://download.acestream.media/linux/acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz" && \
    tar zxf acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz && \
    rm acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz

# 🐍 Install engine + proxy Python dependencies
RUN pip install --no-cache-dir \
    pycryptodome lxml apsw psutil pynacl iso8601 aiohttp flask requests gunicorn gevent

# 📂 Copy proxy and startup script
COPY server.py .
COPY start.sh .

# ✅ Make sure the script is executable
RUN chmod +x /app/start.sh

# 🌐 Expose only the proxy port
EXPOSE 8888

# 🚀 Launch script that handles port forwarding if needed
ENTRYPOINT ["/app/start.sh"]
