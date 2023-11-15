# git-chat

Todo:

- Mesajlar seen bilgisi içermemeli. Onun yerine her kullanıcı için ayrı bir dosya tutulup gördüğü son mesaj yazmalı. Ancak bu bir indisse mesaj silme durumunda güncelleme olmalı. En iyisi mesaj silince mesaj içeriğini "[DELETED]" gibi özel bir şekle çevirmek. Bunları arayüzde göstermeyebiliriz.

Future work:

- Probably use a db file. (Especially for easier searching and editing.)
- Group chats + mentions, etc.
- Attachments (images, videos, audio, files, etc.)
- Notifications (unseen emergency messages)
- Read receipts (seen)
- Typing indicators (typing)
- Presence (online, offline, away, etc.)
- Emojis, formatting, links, code, etc. (Maybe use markdown?)
- Search (by user, by time, by content, by media type etc.)
- Edit/delete (unseen) messages
- Emergency/silent messages
- Message threads (like Slack) including replies and reactions -- each thread is stored as a separate file -- also channels?
- Mark as unread
- More than messaging
  - Tasks (assigning tasks to users, etc.), Calendar, Kanban board?
  - Notes and documents

A better idea:

- Use Obsidian.
- Maybe use Chat View plugin to display messages.
- Create an Obsidian plugin or Python daemon (<https://pypi.org/project/python-daemon/>). If it is a plugin, we can use Obsidian to send messages as well. We can also show messages in a separate pane like Day Planner.
- Share Obsidian notes folder with other users.
- Tasks and calendar. "Kanban" and "Projects". Dashboard and custom notes.
