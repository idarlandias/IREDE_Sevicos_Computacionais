FROM python:3.11-slim

# Install Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Setup working directory for API
WORKDIR /app

# Copy requirements (if any, but we'll install directly for simplicity in this demo)
# COPY requirements.txt .
RUN pip install fastapi uvicorn prometheus-client

# Setup Cron for Backup simulation
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/log/cron

# Copy App Source
COPY app /app/app

# Copy Web Assets
COPY web /usr/share/nginx/html

# Copy Nginx Config
COPY nginx/nginx.conf /etc/nginx/sites-available/default

# Setup Backup Script
COPY backup_script.sh /usr/local/bin/backup_script.sh
RUN chmod +x /usr/local/bin/backup_script.sh

# Setup Cron Job (Run every minute for demo purposes, instead of 24h)
RUN echo "* * * * * /usr/local/bin/backup_script.sh >> /var/log/cron/backup.log 2>&1" > /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron
RUN crontab /etc/cron.d/backup-cron

# Create data directory for volume mapping
RUN mkdir -p /data
RUN chmod 777 /data

# Setup Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port (Cloud Run defaults to 8080)
EXPOSE 8080

# Environment Variables
ENV PORT=8080
ENV APP_ENV=production

CMD ["/entrypoint.sh"]
