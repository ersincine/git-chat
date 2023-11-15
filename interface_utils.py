from utils import run_command


def clear_screen() -> None:
    run_command(["clear"])


def yes_no_prompt(prompt: str, default_yes: bool = True) -> bool:
    if default_yes:
        return input(prompt + " [Y/n] ").lower() != "n"
    return input(prompt + " [y/N] ").lower() != "y"
