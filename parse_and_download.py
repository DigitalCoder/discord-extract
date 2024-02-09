import json
import requests
import os
import re

# Définir l'occurrence spécifique à rechercher
occurrence_specifique = "@d1g1talc0d3r"

def parse_and_download(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    total_items = len(data)  # Nombre total d'éléments à traiter
    print(f"Début du traitement de {total_items} éléments.")

    for index, item in enumerate(data):
        id = item['id']
        content = item['content']

        # Vérifie si l'occurrence spécifique est présente dans 'content'
        if occurrence_specifique in content:
            print(f"\nTraitement de l'élément {index + 1}/{total_items} avec ID: {id} contenant {occurrence_specifique}")

            prompt_search = re.search(r'`(.+?)`', content)
            prompt_text = prompt_search.group(1) if prompt_search else ''
            if prompt_text:
                print(f"Prompt trouvé : {prompt_text}")

            if 'embeds' in item:
                session_id = item['embeds'][0]['url'].split('/')[3]
                print(f"Session ID: {session_id}")
                dir_path = f'upload/{session_id}'
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                prompt_file_path = os.path.join(dir_path, f'prompt_{session_id}.txt')
                with open(prompt_file_path, 'w') as prompt_file:
                    prompt_file.write(prompt_text)
                    print(f'Prompt enregistré : {prompt_file_path}')

                for i, embed in enumerate(item['embeds']):
                    if 'url' in embed:
                        url = embed['url']
                        print(f"Téléchargement de l'image à l'URL: {url}")
                        file_name = f'{id}_{i}.png'
                        file_path = os.path.join(dir_path, file_name)
                        if not os.path.exists(file_path):
                            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                            if response.status_code == 200:
                                with open(file_path, 'wb') as img_file:
                                    img_file.write(response.content)
                                print(f"Image téléchargée: {file_name}")
                            else:
                                print(f"Échec du téléchargement de l'image {file_name}, Statut HTTP: {response.status_code}")
                        else:
                            print(f'Le fichier {file_name} existe déjà.')
        else:
            print(f"\nL'élément {index + 1}/{total_items} avec ID: {id} ne contient pas l'occurrence {occurrence_specifique} et sera ignoré.")

def process_all_json_files(directory):
    # Récupérer tous les fichiers .json dans le répertoire
    json_files = [file for file in os.listdir(directory) if file.endswith(".json")]
    total_files = len(json_files)
    print(f"Nombre total de fichiers JSON à traiter : {total_files}")

    for index, file in enumerate(json_files):
        json_file_path = os.path.join(directory, file)
        print(f"\nTraitement du fichier {index + 1}/{total_files} : {json_file_path}")
        parse_and_download(json_file_path)  # Votre fonction existante pour traiter chaque fichier

        # Renommer le fichier JSON traité en ajoutant l'extension .ok
        os.rename(json_file_path, json_file_path + ".ok")
        print(f"Fichier traité et renommé en : {json_file_path}.ok")

# Exemple d'utilisation avec le répertoire "/json"
process_all_json_files('json')
