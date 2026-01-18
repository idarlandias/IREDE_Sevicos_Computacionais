FROM python:3.11-slim

# Install Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Setup working directory for API
WORKDIR /app

# Copy requirements (if any, but we'll install directly for simplicity in this demo)
# COPY requirements.txt .
RUN pip install fastapi uvicorn

# Copy App Source
COPY app /app/app

# Copy Web Assets
COPY web /usr/share/nginx/html

# Copy Nginx Config
COPY nginx/nginx.conf /etc/nginx/sites-available/default

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
