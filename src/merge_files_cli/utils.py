import click


def log_info(message: str):
    """
    Log an informational message.
    """
    click.secho(message, fg="blue")


def log_warning(message: str):
    """
    Log a warning message.
    """
    click.secho(message, fg="yellow")


def log_success(message: str):
    """
    Log a success message.
    """
    click.secho(message, fg="bright_green", bold=True)


def log_failure(message: str):
    """
    Log a failure message.
    """
    click.secho(message, fg="bright_red", bold=True)
