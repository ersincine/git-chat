import time

from utils import run_command


def git_clone(url: str) -> tuple[str, bool]:
    return run_command(["git", "clone", url])


def git_pull() -> bool:
    output, success,  = run_command(["git", "pull"])
    assert success
    pulled = "Already up to date." not in output
    return pulled


def git_add(file_path: str) -> None:
    run_command(["git", "add", file_path])


def git_commit(message: str) -> bool:
    committed, output = run_command(["git", "commit", "-m", f"\"{message}\""], critical=False)
    if not committed:
        assert "nothing to commit" in output
    return committed


def git_push() -> None:
    run_command(["git", "push", "origin", "main"])


def current_user() -> str:
    return run_command(["git", "config", "user.name"])[0].strip()


def current_time() -> str:
    return time.strftime("%Y.%m.%d %H:%M")
