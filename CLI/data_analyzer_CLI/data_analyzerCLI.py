import click
from csv_loader import load_csv
from analysis import data_overview, filter_rows, sort_data, missing_values, group_and_aggregate

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

@main.command()
@click.pass_context
@click.option("-c", "--column", prompt="Enter the column to filter", help="Column to filter")
@click.option("-v", "--value", prompt="Enter the value to filter", help="Value to filter")
def filter(ctx, column, value):
    df = ctx.obj["FILE"]
    try:
        filtered_data = filter_rows(df, column, value)
    except KeyError:
        return click.echo(f"No column named {column}")
        
    click.echo(filtered_data)

@main.command()
@click.pass_context
@click.option("-c", "--column", prompt="Enter the column to filter", help="Column to filter")
@click.option("--desc", is_flag=True, help="Descending order")
def sort(ctx, column, desc):
    df = ctx.obj["FILE"]
    try:
        if desc:
            sorted_data = sort_data(df, column, False)
        else:
            sorted_data = sort_data(df, column)
    except KeyError:
        return click.echo(f"No column named {column}")
    
    click.echo(sorted_data)

@main.command()
@click.pass_context
def missing(ctx):
    df = ctx.obj["FILE"]
    missing_dict = missing_values(df)
    click.echo("Missing Values:")
    for key, value in missing_dict.items():
        click.echo(f"- {key}: {value}")

@main.command()
@click.pass_context
@click.option("-g", "--group", prompt="Enter the group column", help="Group Column to filter")
@click.option("-a", "--agg", prompt="Enter the aggregation column", help="Aggregated column to calculate")
@click.option("-o", "--operation", 
    type=click.Choice(['mean', 'sum', 'count', 'min', 'max']), 
    prompt="Enter the type of operation [mean, sum, count, min, max]", help="The operation to perform"
    )
def group(ctx, group, agg, operation):
    df = ctx.obj["FILE"]
    try:
        collected_data = group_and_aggregate(df, group, agg, operation)
    except KeyError as e:
        click.echo(f"Column Selection failed")
        click.echo(f"Details: {e}")
        return
    except ValueError as e:
        click.echo(f"Invalid input parameters")
        click.echo(f"Details: {e}")
        return
    
    click.echo(collected_data)
if __name__ == "__main__":
    main()