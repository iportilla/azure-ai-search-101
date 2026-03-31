from rich.console import Console
from rich.table import Table

console = Console()


def render_product_results(results, title: str = "Search Results", show_reranker: bool = False) -> None:
    table = Table(title=title, show_lines=True)

    table.add_column("Score", justify="right", style="cyan", width=8)
    if show_reranker:
        table.add_column("Reranker", justify="right", style="magenta", width=9)
    table.add_column("Name", style="bold", width=30)
    table.add_column("SKU", width=14)
    table.add_column("Categories", style="blue", width=20)
    table.add_column("Price", justify="right", style="green", width=8)
    table.add_column("Description", width=40)

    for result in results:
        score = f"{result.get('@search.score', 0.0):.4f}"
        name = result.get("name", "")
        sku = result.get("sku", "")
        price = f"${result.get('price', 0):.2f}"
        description = result.get("description", "")
        categories = ", ".join(result.get("categories", []))

        row = [score]
        if show_reranker:
            reranker_score = result.get("@search.rerankerScore")
            row.append(f"{reranker_score:.4f}" if reranker_score is not None else "—")
        row += [name, sku, categories, price, description]

        table.add_row(*row)

    console.print(table)
