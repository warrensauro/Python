import click
import json
import os

PRIORITIES= {
    "o": "optional",
    "l": "low",
    "m": "medium",
    "h": "high",
    "c": "crucial"
}
STATUS= {
    "i": "in progress",
    "c": "completed",
    "d": "deleted"
}
@click.group()
def main():
    pass

@main.command()
@click.option("-n", "--name", prompt="Enter the todo name", help="The todo name")
@click.option("-d", "--desc", prompt="Enter the todo description", help="The todo desciption")
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()), default="m", help="Priority level: o=optional, l=low, m=medium, h=high, c=crucial")
@click.option("-s", "--status", type=click.Choice(STATUS.keys()), default="i", help="Status: i=in progress, c=completed, d=deleted")
@click.option("-f", "--filename", type=click.Path(), default="json/todoCLI.json")
def add_todo(name, desc, priority, status, filename):
    file = ensure_directory(filename)
    data = load_data(file)
    for item in data:
        if item["name"] == name:
            return click.echo(f"Todo name exist: {name}")
    if data:
        new_id = max(item.get("id", 0) for item in data) + 1
    else:
        new_id = 1
    data.append({"id": new_id, "name": name, "description": desc, "priority": PRIORITIES[priority], "status": STATUS[status]})
    click.echo(f"Added todo: {name}")
    save_data(file, data)

@main.command()
@click.option("-f", "--filename", type=click.Path(), default="json/todoCLI.json")
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()), help="Priority level: o=optional, l=low, m=medium, h=high, c=crucial")
@click.option("-s", "--status", type=click.Choice(STATUS.keys()), help="Status: i=in progress, c=completed, d=deleted")
def list_todo(filename, priority, status):
    file = ensure_directory(filename)
    data = load_data(file)
    if not data:
        return click.echo("No todos!")
    output = []
    for item in data:
        keep_item = True
        if item['status'] == STATUS['d'] and status != "d":
                keep_item = False
        if priority is not None:
            if item['priority'] != PRIORITIES[priority]:
                keep_item = False
        if status is not None:
            if item['status'] != STATUS[status]:
                keep_item = False
        if keep_item:
            output.append(item)
    if not output:
        return click.echo(f"No matching todos found!")
    else:
        for item in output:
            click.echo(f"{item['id']} [{item['priority']}] [{item['status']}] | {item['name']} - {item['description']}")

@main.command()
@click.argument("id", type=int, prompt="Enter the todo ID: ", help="Todo ID to delete")
@click.option("-f", "--filename", type=click.Path(), default="json/todoCLI.json")
def delete_todo(id, filename):
    file = ensure_directory(filename)
    data = load_data(file)
    found = False
    for item in data:   
        if item["id"] == id:
            found= True
            item["status"] = STATUS['d']
            click.echo(f"Deleted todo: [{item['priority']}] [{item['status']}] |{item['name']} - {item['description']}")
            save_data(file, data)
            break
    if not found:
        click.echo("Todo not found!")

def ensure_directory(filepath):
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    return filepath
def load_data(file):
    if not os.path.exists(file):
        data = []
    else:
        with open(file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data= []
    return data
def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()