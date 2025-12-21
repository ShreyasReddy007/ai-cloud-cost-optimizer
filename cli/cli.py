from rich.console import Console
from rich.prompt import Prompt

console = Console()


def show_menu() -> str:
    console.print("\n[bold cyan]AI Cloud Cost Optimizer[/bold cyan]")
    console.print("1. Enter new project description")
    console.print("2. Run complete cost analysis")
    console.print("3. View recommendations")
    console.print("4. Export report")
    console.print("5. Exit")

    return Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])
