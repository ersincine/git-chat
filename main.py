from enum import Enum
import os
from re import M
import subprocess

# For now, assume that the messaging happens between two users.

"""
Future work:
- Group chats + mentions, etc.
- Attachments (images, videos, audio, files, etc.)
- Notifications (unseen emergency messages)
- Read receipts (seen)
- Typing indicators (typing)
- Presence (online, offline, away, etc.)
- Emojis, formatting, links, code, etc.
- Search (by user, by time, by content, by media type etc.)
- Edit/delete (unseen) messages
- Emergency/silent messages
- Message threads (like Slack) including replies and reactions -- each thread is stored as a separate file
- Mark as unread
- More than messaging
    - Tasks (assigning tasks to users, etc.), Calendar, Kanban board?
    - Notes and documents
"""

def run_command(command: list[str], critical: bool=True) -> tuple[str, bool]:
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    output = p.stdout.read().decode("utf-8")
    success = p.wait() == 0
    if critical:
        assert success, output
    return output, success


class MessageMode(Enum):
    NORMAL = 0
    EMERGENCY = 1
    IMPORTANT = 2
    EMERGENCY_AND_IMPORTANT = 3

    def __str__(self) -> str:
        return self.name.lower()
    
    @staticmethod
    def from_string(mode_string: str) -> "MessageMode":
        return MessageMode[mode_string.upper()]


class Message:

    @staticmethod
    def from_string(message_string: str) -> "Message":
        lines = message_string.split("\n")
        return Message("\n".join(lines[:-3]), lines[-3], lines[-2], MessageMode.from_string(lines[-1]))

    def __init__(self, content: str, sender: str, time: str, mode: MessageMode) -> None:
        assert "\n\n" not in content
        self.content = content
        self.sender = sender
        self.time = time
        self.mode = mode

    def __str__(self) -> str:
        return f"{self.content}\n{self.sender}\n{self.time}\n{self.mode}\n\n"


def connect(url: str, path: str) -> None:
    repo = url.split("/")[-1].split(".")[0]
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)
    if os.path.exists(os.path.join(path, repo)):
        os.chdir(repo)
        run_command(["git", "pull"])
    else:
        run_command(["git", "clone", url])
        os.chdir(repo)


def send_message(message: Message) -> None:
    with open("messages.txt", "a") as f:
        f.write(str(message))
    os.system("git add messages.txt")
    os.system("git commit -m \"new message\"")
    os.system("git push origin main")


def get_messages() -> list[Message]:
    run_command(["git", "pull"])
    with open("messages.txt", "r") as f:
        text = f.read()
    message_strings = text.split("\n\n")
    return [Message.from_string(message_string) for message_string in message_strings if message_string != ""]


def clear_conversation() -> None:
    with open("messages.txt", "w") as f:
        f.write("")
    os.system("git add messages.txt")
    os.system("git commit -m \"clear conversation\"")
    os.system("git push origin main")


def main() -> None:
    url = "https://github.com/ersincine/sample-chat.git"
    path = "./"
    connect(url, path)
    #clear_conversation()
    #exit()
    send_message(Message("hello 2", "ersincine", "12:00", MessageMode.SILENT))
    messages = get_messages()
    for message in messages:
        print(str(message))
    # clear_conversation()

if __name__ == "__main__":
    main()
