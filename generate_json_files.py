import json
import os
from datetime import datetime

def generate_json_files(upload_dir):
    # Itération à travers tous les sous-répertoires de upload_dir
    for root, dirs, files in os.walk(upload_dir):
        for dir_name in dirs:
            # Construction du chemin complet vers le répertoire actuel
            session_path = os.path.join(root, dir_name)
            # Extraction de date_str et session_id du chemin
            parts = session_path.split(os.sep)
            if len(parts) >= 3:
                date_str = parts[-2]
                session_id = parts[-1]

                image_files = [f for f in os.listdir(session_path) if f.endswith('.png')]
                prompt_files = [f for f in os.listdir(session_path) if f.startswith('prompt_') and f.endswith('.txt')]

                if image_files and prompt_files:
                    prompt_file_path = os.path.join(session_path, prompt_files[0])

                    # Formatage du timestamp pour le nom du fichier JSON
                    try:
                        timestamp = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y%m%d')
                    except ValueError:
                        timestamp = "unknown_date"

                    json_data = {
                        "id": session_id,
                        "date": date_str,
                        "prompt": prompt_file_path,
                        "images": [os.path.join(session_path, img) for img in image_files]
                    }

                    # Le fichier JSON est stocké au même niveau que le répertoire de la session
                    json_filename = f"{timestamp}_{session_id}.json"
                    # json_path = os.path.join(root, json_filename)
                    # stockage au niveau de upload_dir
                    json_path = os.path.join(upload_dir, json_filename)

                    with open(json_path, 'w') as json_file:
                        json.dump(json_data, json_file, indent=4)
                    
                    print(f"Fichier JSON généré : {json_path}")

upload_dir = 'upload'  # Remplacez ceci par le chemin réel vers le répertoire upload
generate_json_files(upload_dir)
