import os
import json
from poetpy import get_poetry

FOLDER = "json"
FILE = "read_poems.json"
FILEPATH = os.path.join(FOLDER, FILE)
def load_data():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    if not os.path.exists(FILEPATH):
        data = []
    else:
        with open(FILEPATH, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
    return data
def save_data(data):
     with open(FILEPATH, "w") as f:
          json.dump(data, f, indent=2)

def get_poem(max_retries=10):
    poem_history = load_data()

    while max_retries:
        try:
            response = get_poetry("random", "1")
        except Exception as e:
            print(f"Unable to read PoetryDB ({e})")
            return None

        if not response or not isinstance(response, list):
            print("Error: Failed to retrieve data from PoetryDB")
            return None

        poem_dict = response[0]
        title = poem_dict.get("title", "Untitled").strip()
        author = poem_dict.get("author", "").strip()

        found = False
        for item in poem_history:
            same_title = item.get('title', '').lower() == title.lower()
            same_author = item.get('author', '').lower() == author.lower()

            if same_title and same_author:
                found = True
                break
        
        if found:
            max_retries -= 1
            continue

        if poem_history:
            new_id = max(item.get('id', 0) for item in poem_history) + 1
        else:
            new_id = 1

        data = {
            'id': new_id,
            'title': title,
            'author': author
        }
        poem_history.append(data)
        save_data(poem_history)
        return poem_dict
    
    print("Alert: Reached maximum retries. No unread unique poems were found. Retry")
    return None

if __name__ == "__main__":
    poem = get_poem()

    if poem:
        print(f"Title : {poem.get('title', 'Untitled')}")
        print(f"Author: {poem.get('author', 'No author')}\n")

        for line in poem.get('lines', []):
            print(line)