# Telegram Bot Starter (Python + Render)

A minimal aiogram 3 bot with `/start`, `/help`, `/id`, an admin check, and an HTTP health endpoint.

## Configure

Set these environment variables in Render:

- `BOT_TOKEN`: token from BotFather. Keep it secret.
- `ADMIN_IDS`: comma-separated Telegram numeric user IDs, e.g. `123456789,987654321`.
- `PORT`: optional; Render supplies this automatically.

## Deploy

1. Create a GitHub repository and upload these files.
2. In Render, create a new **Background Worker** from that repository.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `python main.py`.
5. Add `BOT_TOKEN` and `ADMIN_IDS` as secret environment variables.
6. Deploy and message your bot with `/start`.

Do not commit bot tokens or other secrets to GitHub.
