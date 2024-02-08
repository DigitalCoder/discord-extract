#!/bin/sh
# Ajuster les permissions du répertoire upload
chmod -R 777 /upload
# Exécuter le script Python principal
exec python ./parse_and_download.py
