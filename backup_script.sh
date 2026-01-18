#!/bin/bash
# Backup script to run via cron
BACKUP_DIR="/data/backups"
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
cp /data/visitas.json $BACKUP_DIR/backup_visitas_$TIMESTAMP.json 2>/dev/null
echo "[$(date)] Backup realizado: backup_visitas_$TIMESTAMP.json" >> /data/logs.txt
