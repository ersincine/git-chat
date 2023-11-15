import os
from typing import Optional

from git_utils import current_user


def _get_text_path(dir_path: Optional[str]=None) -> str:
    file_name = "messages.txt"
    if dir_path is None:
        dir_path = os.getcwd()
    return os.path.join(dir_path, file_name)


def text_read() -> str:
    if not os.path.exists(_get_text_path()):
        return ""
    with open(_get_text_path(), "r") as f:
        return f.read()


def text_write(content: str) -> None:
    with open(_get_text_path(), "w") as f:
        f.write(content)


def text_clear() -> None:
    text_write("")


def text_append(content: str) -> None:
    with open(_get_text_path(), "a") as f:
        f.write(content)


def _get_seen_path(dir_path: Optional[str]=None) -> str:
    file_name = "seen.csv"
    if dir_path is None:
        dir_path = os.getcwd()
    return os.path.join(dir_path, file_name)


def _seen_read() -> list[str]:
    if not os.path.exists(_get_seen_path()):
        return []
    with open(_get_seen_path(), "r") as f:
        return f.read().splitlines()[1:]


def _seen_write(rows: list[str]) -> None:
    with open(_get_seen_path(), "w") as f:
        f.write("User,Seen\n")  # Username and last seen index.
        for row in rows:
            assert row.count(",") == 1
            f.write(row + "\n")


def seen_clear() -> None:
    _seen_write([])


def get_last_seen_idx(user: str=current_user()) -> int:
    rows = _seen_read()
    for row in rows:
        candidate_user, candidate_last_seen_idx = row.split(",")
        if candidate_user == user:
            return int(candidate_last_seen_idx)
    return -1


def set_last_seen_idx(last_seen_idx: int, user: str=current_user()) -> None:
    rows = _seen_read()
    for i, row in enumerate(rows):
        candidate_user, _ = row.split(",")
        if candidate_user == user:
            rows[i] = f"{user},{last_seen_idx}"
            _seen_write(rows) # Update
            return
    rows.append(f"{user},{last_seen_idx}")
    _seen_write(rows)  # Append
