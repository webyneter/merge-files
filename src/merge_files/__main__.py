"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Merge Files."""


if __name__ == "__main__":
    main(prog_name="merge-files")  # pragma: no cover
