import json
import os

def extract_prompt_text(prompt_file_path):
    """Extrait le texte du fichier prompt."""
    with open(prompt_file_path, 'r') as file:
        return file.read().strip()

def generate_hashtags_from_text(text):
    """Génère des hashtags à partir du texte du prompt."""
    words = text.split()
    hashtags = [f"#{word.lower()}" for word in words if len(word) > 3]
    return hashtags

def process_json_files(json_directory):
    """Traite chaque fichier JSON pour extraire les prompts et générer des hashtags."""
    for file in os.listdir(json_directory):
        if file.endswith(".json"):
            json_path = os.path.join(json_directory, file)
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
                prompt_path = data['prompt']
                prompt_text = extract_prompt_text(prompt_path)
                hashtags = generate_hashtags_from_text(prompt_text)
                
                # Générer le chemin du fichier de hashtags
                hashtags_file_path = prompt_path.replace('prompt_', 'hashtags_')
                with open(hashtags_file_path, 'w') as hashtags_file:
                    hashtags_file.write(' '.join(hashtags))
                print(f"Hashtags sauvegardés dans {hashtags_file_path}")

json_directory = 'upload'  # Remplacez par le chemin réel
process_json_files(json_directory)
