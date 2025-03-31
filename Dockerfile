FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /openace

# System dependencies
RUN apt update && apt install -y --no-install-recommends \
    wget curl ca-certificates cron logrotate && \
    rm -rf /var/lib/apt/lists/*

# Download and extract AceStream Engine
RUN wget -q "https://download.acestream.media/linux/acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz" && \
    tar zxf acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz && \
    rm acestream_3.2.3_ubuntu_22.04_x86_64_py3.10.tar.gz

# Install engine + proxy Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app, startup script, and logrotate config
COPY app/ /openace/app/
COPY server.py .
COPY start.sh .
COPY logrotate/acestream.conf /etc/logrotate.d/acestream


# Set logrotate permissions and make log files
RUN chmod 644 /etc/logrotate.d/acestream && \
    mkdir -p /var/log/openace && \
    touch /var/log/openace/acestream.log && \
    touch /var/log/openace/proxy.log && \
    chmod 644 /var/log/openace/*.log && \
    chmod +x /openace/start.sh

# Create cron job for logrotate
RUN echo "0 0 * * * /usr/sbin/logrotate /etc/logrotate.conf" > /etc/cron.d/openace && \
    chmod 0644 /etc/cron.d/openace && \
    crontab /etc/cron.d/openace

EXPOSE 8888

ENTRYPOINT ["/openace/start.sh"]
