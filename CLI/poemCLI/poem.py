import os
import json
import click
from poetpy import get_poetry

FOLDER = "json"
FILE = "read_poems.json"
FILEPATH = os.path.join(FOLDER, FILE)

@click.group()
def main():
    pass

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

def display_poem(poem):
    if poem:
        click.echo(f"Title : {poem.get('title', 'Untitled')}")
        click.echo(f"Author: {poem.get('author', 'No author')}\n")

        for line in poem.get('lines', []):
            click.echo(line)

@main.command(name='new')
def new_poem(max_retries=10):
    poem_history = load_data()

    success = False
    while max_retries:
        try:
            response = get_poetry("random", "1")
        except Exception as e:
            click.echo(f"Unable to read PoetryDB ({e})")
            return

        if not response or not isinstance(response, list):
            click.echo("Error: Failed to retrieve data from PoetryDB")
            return

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
        
        display_poem(poem_dict)
        reflection = click.prompt("Write your reflection")
        if poem_history:
            new_id = max(item.get('id', 0) for item in poem_history) + 1
        else:
            new_id = 1

        data = {
            'id': new_id,
            'title': title,
            'author': author,
            'lines': poem_dict.get("lines", []),
            'reflection': reflection
        }
        poem_history.append(data)
        save_data(poem_history)
        success = True
        return
    if not success:
        click.echo("Alert: Reached maximum retries. No unread unique poems were found. Retry")

@main.command()
def history():
    poem_history = load_data()

    if not poem_history:
        click.echo("History empty. Read a poem.")
        return
    for item in poem_history:
        click.echo(
            f"Id:         {item.get('id', '')}\n"
            f"Title:      {item.get('title', '')}\n"
            f"Author:     {item.get('author', '')}\n"
            f"Reflection: {item.get('reflection', '')}\n\n"
        )

@main.command()
@click.argument('id', type=int)
def view(id):
    poem_history = load_data()

    if not poem_history:
        click.echo("History empty. Read a poem.")
        return
    
    found = False
    for item in poem_history:
        if item['id'] == id:
            found = True
            click.echo(
                f"Id:         {item.get('id', '')}\n"
                f"Title:      {item.get('title', '')}\n"
                f"Author:     {item.get('author', '')}\n"
                f"Poem:"
            )
            click.echo('\n'.join(item.get('lines', [])))
            click.echo(
                f"\nReflection: {item.get('reflection', '')}\n"
                )
            return    
    if not found:
        click.echo(f"Poem with id {id} not found.")
if __name__ == "__main__":
    main()