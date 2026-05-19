import click
import json
import os
from datetime import date

PRIORITIES={
    "o": "optional",
    "l": "low",
    "m": "medium",
    "h": "high",
    "c": "crucial"
}
PRIORITIES_COLORS={
    "crucial": "red",
    "high": "bright_red",
    "medium": "yellow",
    "low": "cyan",
    "optional": "blue" 
}
STATUS={
    "i": "in progress",
    "c": "completed",
    "d": "deleted"
}
STATUS_COLORS={
    "in progress": "white",
    "completed": "green",
    "deleted": "bright_black"
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
def format_todo(item):
    p_color = PRIORITIES_COLORS.get(item['priority'], 'white')
    s_color = STATUS_COLORS.get(item['status'], "white")

    due_display = "No due date"
    due_color = "white"
    if item['due_date'] is not None:
        if item['status'] != STATUS["c"]:
            diff = date.fromisoformat(item['due_date']) - date.today()
            days_left = diff.days
            if days_left > 0:
                due_color = "green"
            elif days_left == 0:
                due_color = "yellow"
            else:
                due_color = "red"

        due_display = item['due_date']

    base_info =( 
        f"{click.style(str(item['id']), fg='bright_white')} "
        f"[{click.style(item['priority'], fg=p_color)}] [{click.style(item['status'], fg=s_color)}] "
        f"| {item['name']} - {item['description']} - {item['date_added']} | {click.style(due_display, fg=due_color)} "
    )
    if item['date_completed']:
        formatted_item = f"{base_info}| {click.style(item['date_completed'], fg='green')}"
    else:
        formatted_item = base_info
    return formatted_item

@main.command(name='add')
@click.pass_context
@click.option("-n", "--name", prompt="Enter the todo name", help="The todo name")
@click.option("-d", "--desc", prompt="Enter the todo description", help="The todo desciption")
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys(), case_sensitive=False), default="m", help="Priority level: o=optional, l=low, m=medium, h=high, c=crucial")
@click.option("--due", type=click.DateTime(formats=["%Y-%m-%d"]), default=None, help="Due date (YYYY-MM-DD)")
def add_todo(ctx, name, desc, priority, due):
    file = ctx.obj["FILE"]
    data = load_data(file)
    priority = priority.lower()
    for item in data:
        if item["name"].lower() == name.lower():
            click.echo(f"Todo name exist: {name}")
            return
    if data:
        new_id = max(item.get("id", 0) for item in data) + 1
    else:
        new_id = 1
    data.append({"id": new_id, "name": name, "description": desc, "priority": PRIORITIES[priority],
                 "status": STATUS['i'], "date_added": date.today().isoformat(), "due_date": due.date().isoformat() if due else None,
                 "date_completed": None})
    click.echo(f"Added todo: {name}")
    save_data(file, data)

@main.command(name='list')
@click.pass_context
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys() , case_sensitive=False), help="Priority level: o=optional, l=low, m=medium, h=high, c=crucial")
@click.option("-s", "--status", type=click.Choice(STATUS.keys(), case_sensitive=False), help="Status: i=in progress, c=completed, d=deleted")
@click.option("-y", "--year", type=int, help="Filter by year")
@click.option("-m", "--month", type=click.IntRange(1, 12), help="Filter by month (1-12)")
@click.option("--search", help="Search todo/s name or description")
@click.option("--sort", type=click.Choice(['priority', 'status', 'added', 'due'], case_sensitive=False))
def list_todo(ctx, priority, status, year, month, search, sort):
    file = ctx.obj["FILE"]
    data = load_data(file)
    if not data:
        click.secho("No todos!", fg="red")
        return
    output = []
    for item in data:
        keep_item = True
        todo_date = date.fromisoformat(item['date_added'])
        if item['status'] == STATUS['d'] and status != 'd':
            keep_item = False
        if priority is not None and item['priority'] != PRIORITIES[priority.lower()]:
            keep_item = False 
        if status is not None and item['status'] != STATUS[status.lower()]:
            keep_item = False
        if year is not None and todo_date.year != year:
            keep_item = False
        if month is not None and todo_date.month != month:
            keep_item = False
        if search is not None:
            if search.lower() not in item['name'].lower() and search.lower() not in item['description'].lower():
                keep_item = False 

        if keep_item:
            output.append(item)
    if not output:
        click.secho(f"No matching todos found!", fg="red")
    else:
        if sort is not None:
            if sort.lower() == 'priority':
                priority_order = {
                'crucial': 0,
                'high': 1,
                'medium': 2,
                'low': 3,
                'optional': 4
                }
                output.sort(key=lambda item: priority_order[item['priority']])
            elif sort.lower() == 'status':
                status_order = {
                    'in progress': 0,
                    'completed': 1,
                    'deleted': 2
                }
                output.sort(key=lambda item: status_order[item['status']])
            elif sort.lower() == 'added':
                output.sort(key=lambda item: item['date_added'])
            elif sort.lower() == 'due':
                output.sort(key=lambda item: item['due_date'] or '9999-12-31')
        for item in output:
            click.echo(format_todo(item))

@main.command(name='delete')
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
            new_val = format_todo(item)
            break
    if found:
        click.echo(f"Deleted : {new_val}")
        save_data(file, data)
    else:
        click.secho("Todo not found!", fg="red")

@main.command(name='update')
@click.pass_context
@click.argument("id", type=int)
@click.option("-n", "--name", help="The new todo name")
@click.option("-d", "--desc", help="The new todo description")
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys(), case_sensitive=False), help="Priority level: o=optional, l=low, m=medium, h=high, c=crucial")
@click.option("--due", type=click.DateTime(formats=["%Y-%m-%d"]), default=None, help="Due date (YYYY-MM-DD)")
def update_todo(ctx, id, name, desc, priority, due):
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
            old_val = format_todo(item)
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
                if PRIORITIES[priority.lower()] == item['priority']:
                    click.echo(f"todo already has the priority: {item['priority']}")
                else:
                    item['priority'] = PRIORITIES[priority.lower()]
                    updated = True
            if due is not None:
                due_date = None
                if item['due_date'] is not None:
                    due_date = date.fromisoformat(item['due_date'])
                if due_date and due.date() == due_date:
                    click.echo(f"todo has the due date: {due_date}")
                else:
                    item['due_date'] = due.date().isoformat()
                    updated = True
            new_val = format_todo(item)
            break
    if not found:
        click.secho("Todo not found!", fg="red")
    else:
        if updated:
            click.echo(f"Before: {old_val}")
            click.echo(f"After: {new_val}")
            click.echo("Todo updated")
            save_data(file, data)
        else:
            click.echo("No changes made")

@main.command(name='done')
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
            item['date_completed'] = date.today().isoformat()
            new_val = format_todo(item)
            break
    if found:
        save_data(file, data)
        click.echo(new_val)
        click.secho("Todo completed!", fg="green")
    else:
        click.secho("Todo not found", fg="red")

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
        click.echo(format_todo(item))
    
    if click.confirm("Do you want to trash all deleted todos?", default=False):
        save_data(file, new_data)
        click.secho("Successfully trashed deleted todos!", fg="green")
    else:
        click.secho("Trashing aborted.", fg="red")

@main.command()
@click.pass_context
def today(ctx):
    file = ctx.obj['FILE']
    data = load_data(file)

    shown_data = []
    for item in data:
        if item['due_date'] is not None:
            if item['status'] != STATUS["c"] and item['status'] != STATUS["d"]:
                diff = date.fromisoformat(item['due_date']) - date.today()
                if diff.days == 0:
                    shown_data.append(item)
    if shown_data:
        click.echo(f"{len(shown_data)} todo/s due today:")
        for item in shown_data:
            click.echo(format_todo(item))
    else:
        click.echo("No todos due today!")

@main.command()
@click.pass_context
def overdue(ctx):
    file = ctx.obj['FILE']
    data = load_data(file)

    shown_data = []
    for item in data:
        if item['due_date'] is not None:
            if item['status'] != STATUS["c"] and item['status'] != STATUS["d"]:
                diff = date.fromisoformat(item['due_date']) - date.today()
                if diff.days < 0:
                    shown_data.append(item)
    if shown_data:
        click.echo(f"{len(shown_data)} overdue todo/s:")
        for item in shown_data:
            click.echo(format_todo(item))
    else:
        click.echo("No overdue todos!")

@main.command()
@click.pass_context
@click.option('-d', '--days', type=int, help="Filter by number of days")
def upcoming(ctx, days):
    file = ctx.obj['FILE']
    data = load_data(file)

    shown_data = []
    for item in data:
        if item['due_date'] is not None:
            if item['status'] != STATUS["c"] and item['status'] != STATUS["d"]:
                diff = date.fromisoformat(item['due_date']) - date.today()
                if diff.days > 0:
                    if days is not None:
                        if diff.days <= days:
                            shown_data.append(item)
                    else:
                        shown_data.append(item)
    if shown_data:
        if days is not None:
            click.echo(f"{len(shown_data)} upcoming todos (next {days} days):")
        else:
            click.echo(f"{len(shown_data)} upcoming todos:")
        for item in shown_data:
            click.echo(format_todo(item))
    else:
        click.echo("No upcoming todos!")

@main.command()
@click.pass_context
def stats(ctx):
    file = ctx.obj['FILE']
    data = load_data(file)

    total = 0
    in_progress = 0
    completed = 0
    deleted = 0
    crucial_prio = 0
    high_prio = 0
    due_over = 0
    due_today = 0
    due_upcoming = 0
    for item in data:
        total += 1
        if item['status'] == STATUS['i']:
            in_progress += 1
        if item['status'] == STATUS['c']:
            completed += 1
        if item['status'] == STATUS['d']:
            deleted += 1

        if item['priority'] == PRIORITIES['c']:
            crucial_prio += 1
        if item['priority'] == PRIORITIES['h']:
            high_prio += 1

        if item['due_date'] is not None:
            if item['status'] != STATUS["c"] and item['status'] != STATUS["d"]:
                diff = date.fromisoformat(item['due_date']) - date.today()
                if diff.days < 0:
                    due_over += 1
                if diff.days == 0:
                    due_today += 1
                if diff.days > 0:
                    due_upcoming += 1

    completion_rate = 0
    if (total - deleted) > 0:
        completion_rate = completed / (total - deleted)

    click.echo(f"Total todos     : {total}")
    click.echo(f"In progress     : {in_progress}")
    click.echo(f"Completed       : {completed}")
    click.echo(f"Deleted         : {deleted}")
    click.echo(f"Completion Rate : {completion_rate:.1%}\n")
    click.echo(f"High Priority   : {high_prio}")
    click.echo(f"Crucial Priority: {crucial_prio}\n")
    click.echo(f"Overdue todos   : {due_over}")
    click.echo(f"Due today       : {due_today}")
    click.echo(f"Upcoming todos  : {due_upcoming}")
if __name__ == "__main__":
    main()