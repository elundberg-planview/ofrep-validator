from typing import List
from typing_extensions import Annotated

import httpx
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

def format_flag_output(data, base_url: str, key: str = None):
    """Format the OFREP response for nice display"""
    if key:
        # Single flag response
        console.print(f"\n[bold blue]Flag:[/bold blue] {key}")
        console.print(f"[dim]Endpoint:[/dim] {base_url}/ofrep/v1/evaluate/flags/{key}")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        for prop, value in data.items():
            if isinstance(value, dict):
                value = str(value)
            table.add_row(str(prop), str(value))

        console.print(table)
    else:
        # Multiple flags response
        console.print(f"\n[bold blue]All Flags[/bold blue]")
        console.print(f"[dim]Endpoint:[/dim] {base_url}/ofrep/v1/evaluate/flags")

        for flag in data['flags']:
            flag_key = flag.pop('key')
            key_color = 'bright_green' if flag['value'] else 'bright_red'
            console.print(f"\n[{key_color}]• {flag_key}[/{key_color}]")

            table = Table(show_header=False, show_edge=False, pad_edge=False)
            table.add_column("Property", style="cyan", width=15)
            table.add_column("Value", style="green")

            for prop, value in flag.items():
                if isinstance(value, dict):
                    value = str(value)
                table.add_row(f"  {prop}", str(value))

            console.print(table)

@app.command()
def main(base_url: str, context: Annotated[List[str], typer.Argument()] = None, key: str = None):
    context = context or []
    context_data = dict([item.split('=') for item in context])
    url = f'{base_url}/ofrep/v1/evaluate/flags'

    if key is not None:
        url += f'/{key}'

    try:
        console.print(f"[dim]Requesting:[/dim] {url}")
        r = httpx.post(url, json={'context': context_data})
        r.raise_for_status()

        response_data = r.json()
        format_flag_output(response_data, base_url, key)

    except httpx.HTTPStatusError as e:
        console.print(f"[red]HTTP Error {e.response.status_code}:[/red] {e.response.text}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")


if __name__ == "__main__":
    app()
