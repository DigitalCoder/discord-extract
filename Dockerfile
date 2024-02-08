# Utiliser une image de base Python officielle
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du script Python et les fichiers JSON dans le conteneur
COPY . /app

# Installer les dépendances Python nécessaires
RUN pip install requests

# Créer un utilisateur non-root et passer à cet utilisateur
RUN useradd -m pythonuser
USER pythonuser

# Commande pour exécuter le script Python
CMD ["python", "./parse_and_download.py"]
