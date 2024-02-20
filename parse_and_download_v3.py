import json
import requests
import os
import re
from datetime import datetime

# Définir l'occurrence spécifique à rechercher et le chemin du fichier de log
occurrence_specifique = "@d1g1talc0d3r"
# Initialiser le nom du fichier de log avec le timestamp actuel
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = f"script_log_{current_time}.txt"

def log(message, log_to_file=True):
    print(message)
    if log_to_file:
        with open(log_file_path, "a") as log_file:
            log_file.write(message + "\n")

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.split('T')[0], '%Y-%m-%d').strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return "to_sort"

def parse_and_download(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    total_items = len(data)
    log(f"Début du traitement de {total_items} éléments.")

    prompts_vides = {}

    for index, item in enumerate(data):
        id = item['id']
        content = item['content']
        date_formattee = parse_date(item.get('date'))

        if occurrence_specifique in content:
            log(f"\nTraitement de l'élément {index + 1}/{total_items} avec ID: {id} contenant {occurrence_specifique}")

            ## prompt_search = re.search(r'`(.+?)`', content)
            prompt_search = re.search(r'`((.|\n)+?)`', content)
            
            prompt_text = prompt_search.group(1) if prompt_search else ''
            if prompt_text:
                log(f"Prompt trouvé : {prompt_text}")
            else:
                prompts_vides[json_file] = prompts_vides.get(json_file, []) + [id]

            if 'embeds' in item:
                for i, embed in enumerate(item['embeds']):
                    if 'url' in embed:
                        url = embed['url']
                        session_id = url.split('/')[3]
                        dir_path = f'upload/{date_formattee}/{session_id}'
                        log(f"Chemin de sauvegarde : {dir_path}")
                        if not os.path.exists(dir_path):
                            os.makedirs(dir_path)
                        prompt_file_path = os.path.join(dir_path, f'prompt_{session_id}.txt')
                        with open(prompt_file_path, 'w') as prompt_file:
                            prompt_file.write(prompt_text)
                            log(f'Prompt enregistré : {prompt_file_path}')

                        log(f"Téléchargement de l'image à l'URL: {url}")
                        file_name = f'{id}_{i}.png'
                        file_path = os.path.join(dir_path, file_name)
                        if not os.path.exists(file_path):
                            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                            if response.status_code == 200:
                                with open(file_path, 'wb') as img_file:
                                    img_file.write(response.content)
                                log(f"Image téléchargée: {file_name}")
                            else:
                                log(f"Échec du téléchargement de l'image {file_name}, Statut HTTP: {response.status_code}")
                        else:
                            log(f'Le fichier {file_name} existe déjà.')
                    else:
                        log("Un 'embed' sans 'url' a été trouvé, élément ignoré.")
            else:
                log("Aucun 'embed' trouvé pour cet élément.")
        else:
            log(f"\nL'élément {index + 1}/{total_items} avec ID: {id} ne contient pas l'occurrence {occurrence_specifique} et sera ignoré.")

    if prompts_vides:
        log("\nRésumé des fichiers JSON et IDs de session avec prompts vides:")
        for fichier, ids in prompts_vides.items():
            log(f"Fichier: {os.path.basename(fichier)}, IDs de session: {', '.join(ids)}")

def process_all_json_files(directory):
    json_files = [file for file in os.listdir(directory) if file.endswith(".json")]
    total_files = len(json_files)
    log(f"Nombre total de fichiers JSON à traiter : {total_files}")

    for index, file in enumerate(json_files):
        json_file_path = os.path.join(directory, file)
        log(f"\nTraitement du fichier {index + 1}/{total_files} : {json_file_path}")
        parse_and_download(json_file_path)
        os.rename(json_file_path, json_file_path + ".ok")
        log(f"Fichier traité et renommé en : {json_file_path}.ok")

# S'assurer que le fichier de log est vide au début du script
with open(log_file_path, "w") as log_file:
    log_file.write("")

# Exemple d'utilisation avec le répertoire "/json"
process_all_json_files('json')
