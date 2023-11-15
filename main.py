from calendar import c
from enum import Enum
import os
from typing import Optional

from file_utils import *
from git_utils import *
from interface_utils import *


# For now, assume that the messaging happens between two users.


class Message:

    @staticmethod
    def from_string(message_string: str) -> "Message":
        lines = message_string.split("\n")
        return Message("\n".join(lines[:-2]), lines[-2], lines[-1])

    def __init__(self, content: str, sender: str=current_user(), time: str=current_time()) -> None:
        assert "\n\n" not in content
        self.content = content
        self.sender = sender
        self.time = time

    def __str__(self) -> str:
        return f"{self.content}\n{self.sender}\n{self.time}\n\n"


def connect(url: str, path: str) -> None:
    repo = url.split("/")[-1].split(".")[0]
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)
    if os.path.exists(repo):
        os.chdir(repo)
        pulled = git_pull()
        if pulled:
            print("Local chat database updated.")
        else:
            print("Local chat database is up to date.")
    else:
        git_clone(url)
        print("Local chat database created.")
        os.chdir(repo)


def get_messages(receiver: str=current_user()) -> tuple[list[Message], int]:
    git_pull()
    text = text_read()
    message_strings = text.split("\n\n")
    messages = [Message.from_string(message_string) for message_string in message_strings if message_string != ""]

    last_seen_idx = get_last_seen_idx(receiver)
    return messages, last_seen_idx


def mark_messages_as_seen(last_seen_idx: int, seen_by: str=current_user()) -> None:
    set_last_seen_idx(last_seen_idx, seen_by)
    git_add("seen.csv")
    git_commit("seen messages")
    git_push()
    print("Messages marked as seen.")


def show_messages(messages: list[Message], last_seen_idx: Optional[int]=None, num_previous_messages_to_show: int=1) -> None:
    if num_previous_messages_to_show > 0:
        print("Last seen messages:")
        for seen_message in messages[max(0, last_seen_idx + 1 - num_previous_messages_to_show):last_seen_idx + 1]:
            print(seen_message)
    if last_seen_idx == len(messages) - 1:
        print("No unseen messages.")
    else:
        print("Unseen messages:")
        for message in messages[last_seen_idx + 1:]:
            print(message)
    num_previous_str = input("Enter the number of previous messages to see. (Leave empty to skip.) ")
    if num_previous_str:
        num_previous = int(num_previous_str)
        if num_previous > 0:
            clear_screen()
            show_messages(messages, last_seen_idx, num_previous)


def send_message(message: Message) -> None:
    messages, last_seen_idx = get_messages()
    if last_seen_idx != len(messages) - 1:
        to_see = yes_no_prompt("You have unseen messages. Do you want to see them? (You will still have a chance to send your message.)")
        if to_see:
            show_messages(messages, last_seen_idx)
            mark_messages_as_seen(len(messages) - 1)
            to_send = yes_no_prompt("Still want to send your message?")
            if not to_send:
                print("Message discarded.")
                return

    text_append(str(message))
    git_add("messages.txt")
    mark_messages_as_seen(len(messages))  # Mark the current message as seen.
    git_add("seen.csv")
    git_commit("new message")
    git_push()
    print("Message sent.")


def clear_conversation() -> None:
    text_clear()
    git_add("messages.txt")
    seen_clear()
    git_add("seen.csv")
    commited = git_commit("clear conversation")
    if commited:
        git_push()
        print("Conversation cleared.")
    else:    
        print("Conversation is already clear.")


def main() -> None:
    url = "https://github.com/ersincine/sample-chat.git"
    path = os.getcwd()
    connect(url, path)
    #connect(url, path)
    #send_message(Message("Hello!"))
    #exit()
    #clear_conversation()
    #exit()
    
    messages, _ = get_messages()
    for message in messages:
        print(str(message))
    # clear_conversation()
    

if __name__ == "__main__":
    main()
