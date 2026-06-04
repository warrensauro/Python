import click
from csv_loader import load_csv
from analysis import data_overview

@click.group()
@click.argument("file", type=click.Path())
@click.pass_context
def main(ctx, file):
    ctx.ensure_object(dict)
    try:
       ctx.obj["FILE"] = load_csv(file)
    except FileNotFoundError:
        click.echo(f"File not found: {file}")
        ctx.exit(1)
    except ValueError:
        click.echo(f"Corrupted data in file: {file}")
        ctx.exit(1)

@main.command()
@click.pass_context
def overview(ctx):
    df = ctx.obj["FILE"]
    if not df:
        return
    meta = data_overview(df)
    row_count = meta['rows']
    column_count = meta['column_count']
    column_names = meta['column_names']
    data_types = meta['data_types']

    click.echo(f"Rows: {row_count}")
    click.echo(f"Columns: {column_count}\n")
    click.echo("Column names:")
    for names in column_names:
        click.echo(f"- {names}")
    click.echo("Data types:")
    for name, data_type in data_types.items():
        click.echo(f"- {name} | {data_type}")

if __name__ == "__main__":
    main()