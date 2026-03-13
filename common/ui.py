from __future__ import annotations

from time import sleep


def show_message(text: str) -> None:
    print(text)


def wait_for_continue(prompt: str, auto_advance: bool = False) -> None:
    if auto_advance:
        print(f"{prompt} [auto]")
        return
    input(f"{prompt}\nPress Enter to continue...")


def countdown(seconds: int, label: str) -> None:
    for remaining in range(seconds, 0, -1):
        print(f"{label}: {remaining}s remaining")
        sleep(1)
