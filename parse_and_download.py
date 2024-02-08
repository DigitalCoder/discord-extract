import json
import requests
import os
import re

def parse_and_download(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    total_items = len(data)
    print(f"Début du traitement de {total_items} éléments.")

    for index, item in enumerate(data):
        id = item['id']
        print(f"\nTraitement de l'élément {index + 1}/{total_items} avec ID: {id}")
        content = item['content']
        prompt_search = re.search(r'`(.+?)`', content)
        prompt_text = prompt_search.group(1) if prompt_search else ''

        if 'embeds' in item and any('url' in embed for embed in item['embeds']):
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
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                        }
                        response = requests.get(url, headers=headers)
                        if response.status_code == 200:
                            with open(file_path, 'wb') as img_file:
                                img_file.write(response.content)
                            print(f"Image téléchargée: {file_name}")
                        else:
                            print(f"Échec du téléchargement de l'image {file_name}, Statut HTTP: {response.status_code}")
                    else:
                        print(f'Le fichier {file_name} existe déjà.')

def process_all_json_files(directory):
    for file in os.listdir(directory):
        if file.endswith(".json"):
            json_file_path = os.path.join(directory, file)
            print(f"Traitement du fichier : {json_file_path}")
            parse_and_download(json_file_path)

# Exemple d'utilisation avec le répertoire "/json"
process_all_json_files('/json')
