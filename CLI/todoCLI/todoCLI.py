import click
import json
import os
from datetime import date

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
@click.option("-f", "--filename", type=click.Path(), default="json/todoCLI.json", help="Todo JSON file")
@click.pass_context
def main(ctx, filename):
    ctx.ensure_object(dict)
    ctx.obj["FILE"] = ensure_directory(filename)

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

@main.command()
@click.pass_context
@click.option("-n", "--name", prompt="Enter the todo name", help="The todo name")
@click.option("-d", "--desc", prompt="Enter the todo description", help="The todo desciption")
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()), default="m", help="Priority level: o=optional, l=low, m=medium, h=high, c=crucial")
def add_todo(ctx, name, desc, priority):
    file = ctx.obj["FILE"]
    data = load_data(file)
    for item in data:
        if item["name"] == name:
            click.echo(f"Todo name exist: {name}")
            return
    if data:
        new_id = max(item.get("id", 0) for item in data) + 1
    else:
        new_id = 1
    data.append({"id": new_id, "name": name, "description": desc, "priority": PRIORITIES[priority], "status": STATUS['i'], "date_added": date.today().isoformat()})
    click.echo(f"Added todo: {name}")
    save_data(file, data)

@main.command()
@click.pass_context
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()), help="Priority level: o=optional, l=low, m=medium, h=high, c=crucial")
@click.option("-s", "--status", type=click.Choice(STATUS.keys()), help="Status: i=in progress, c=completed, d=deleted")
@click.option("-y", "--year", type=int, help="Filter by year")
@click.option('-m', "--month", type=click.IntRange(1, 12), help="Filter by month (1-12)")
def list_todo(ctx, priority, status, year, month):
    file = ctx.obj["FILE"]
    data = load_data(file)
    if not data:
        click.echo("No todos!")
        return
    output = []
    for item in data:
        keep_item = True
        todo_date = date.fromisoformat(item['date_added'])
        if item['status'] == STATUS['d'] and status != 'd':
            keep_item = False
        if priority is not None and item['priority'] != PRIORITIES[priority]:
            keep_item = False 
        if status is not None and item['status'] != STATUS[status]:
            keep_item = False
        if year is not None and todo_date.year != year:
            keep_item = False
        if month is not None and todo_date.month != month:
            keep_item = False
        if keep_item:
            output.append(item)
    if not output:
        click.echo(f"No matching todos found!")
    else:
        for item in output:
            click.echo(f"{item['id']} [{item['priority']}] [{item['status']}] | {item['name']} - {item['description']} - {item['date_added']}")

@main.command()
@click.pass_context
@click.argument("id", type=int)
def delete_todo(ctx, id):
    file = ctx.obj["FILE"]
    data = load_data(file)
    found = False
    new_val = ''
    for item in data:   
        if item["id"] == id:
            found = True
            if item['status'] == STATUS["d"]:
                click.echo("Todo is marked 'deleted'")
                return
            item["status"] = STATUS['d']
            new_val = f"[{item['priority']}] [{item['status']}] | {item['name']} - {item['description']} - {item['date_added']}"
            break
    if found:
        click.echo(f"Deleted : {new_val}")
        save_data(file, data)
    else:
        click.echo("Todo not found!")

@main.command()
@click.pass_context
@click.argument("id", type=int)
@click.option("-n", "--name", help="The new todo name")
@click.option("-d", "--desc", help="The new todo description")
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()), help="Priority level: o=optional, l=low, m=medium, h=high, c=crucial")
def update_todo(ctx, id, name, desc, priority):
    file = ctx.obj["FILE"]
    data = load_data(file)
    found = False
    updated = False
    old_val = ''
    new_val = ''
    for item in data:
        if item["id"] == id:
            found = True
            if item['status'] == STATUS["d"]:
                click.echo("Todo is marked 'deleted'")
                return
            if item['status'] == STATUS["c"]:
                click.echo("Todo completed, cannot update")
                return
            old_val = f"{item['id']} [{item['priority']}] [{item['status']}] | {item['name']} - {item['description']} - {item['date_added']}"
            if name is not None:
                if name == item['name']:
                    click.echo(f"todo already has the name: {item['name']}")
                else:
                    item['name'] = name
                    updated = True
            if desc is not None:
                if desc == item['description']:
                    click.echo(f"todo already has the description: {item['description']}")
                else:
                    item['description'] = desc
                    updated = True
            if priority is not None:
                if PRIORITIES[priority] == item['priority']:
                    click.echo(f"todo already has the priority: {item['priority']}")
                else:
                    item['priority'] = PRIORITIES[priority]
                    updated = True
            new_val = f"{item['id']} [{item['priority']}] [{item['status']}] | {item['name']} - {item['description']} - {item['date_added']}"
            break
    if not found:
        click.echo("Todo not found!")
    else:
        if updated:
            click.echo(f"Before: {old_val}")
            click.echo(f"After: {new_val}")
            click.echo("Todo updated")
            save_data(file, data)
        else:
            click.echo("No changes made")

@main.command()
@click.pass_context
@click.argument("id", type=int)
def done_todo(ctx, id):
    file = ctx.obj["FILE"]
    data = load_data(file)
    found = False
    new_val = ''
    for item in data:
        if item['id'] == id:
            if item['status'] == STATUS["c"]:
                click.echo("Todo is already 'completed'")
                return
            if item['status'] == STATUS["d"]:
                click.echo("Todo is marked 'deleted'")
                return
            found = True
            item['status'] = STATUS["c"]
            new_val = f"{item['id']} [{item['priority']}] [{item['status']}] | {item['name']} - {item['description']} - {item['date_added']}"
            break
    if found:
        save_data(file, data)
        click.echo(new_val)
        click.echo("Todo completed!")
    else:
        click.echo("Todo not found")

@main.command()
@click.pass_context
def trash(ctx):
    file = ctx.obj["FILE"]
    data = load_data(file)
    
    deleted_items = [item for item in data if item['status'] == STATUS["d"]]
    new_data = [item for item in data if item['status'] != STATUS["d"]]

    if not deleted_items:
        click.echo("No deleted todos.")
        return
    click.echo("Items marked for permanent deletion:")
    for item in deleted_items:
        click.echo(f"{item['id']} [{item['priority']}] [{item['status']}] | {item['name']} - {item['description']} - {item['date_added']}")
    
    if click.confirm("Do you want to trash all deleted todos?", default=False):
        save_data(file, new_data)
        click.echo("Successfully trashed deleted todos!")
    else:
        click.echo("Trashing aborted.")
if __name__ == "__main__":
    main()