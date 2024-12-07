# Slack Anki Reminder Bot

## Overview
This Slack bot integrates with [Anki](https://apps.ankiweb.net/) via the [AnkiConnect](https://foosoft.net/projects/anki-connect/) add-on to provide daily reminders of due flashcards. At a configured time each day, it will post a message in a Slack channel (or directly to you) showing how many Anki cards are due for review and listing their prompts (front fields).

## Features
- **Daily Automated Reminders:** The bot runs at a scheduled time (using `cron`) to fetch due card counts.
- **Slack Integration:** Automatically posts to your chosen Slack channel.
- **AnkiConnect Compatibility:** Works with your local Anki setup and the AnkiConnect add-on.
- **Configurable:** Easily change the reminder time, Slack channel, and environment settings.

## Prerequisites

### Environment Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/anki-slack-reminder.git
   cd anki-slack-reminder
   ```

2. **Set Up Environment Variables:**
   Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   
   Add the following variables to your `.env` file:
   ```bash
   SLACK_BOT_TOKEN=xoxb-your-token-here
   SLACK_CHANNEL=#your-channel-name
   ANKI_CONNECT_URL=http://localhost:8765
   ```

### Anki & AnkiConnect
1. Install [Anki](https://apps.ankiweb.net/) on your computer.
2. Install the [AnkiConnect](https://foosoft.net/projects/anki-connect/) add-on (ID: 2055492159) in Anki.
3. Keep Anki running, as AnkiConnect only works when Anki is open.

### Python & Dependencies
1. **Conda Environment (Optional but Recommended):**
   ```bash
   conda create -n anki_slack_reminder python=3.9
   conda activate anki_slack_reminder
   ```
   
2. **Install Dependencies:**
   ```bash
   pip install requests slack_sdk
   ```

### Slack App & Bot Token
1. Go to [https://api.slack.com/apps](https://api.slack.com/apps) and create a new Slack app.
2. Assign it to your desired Slack workspace.
3. Under **OAuth & Permissions**, add the `chat:write` scope.
4. Install the app to your workspace.
5. Copy the **Bot User OAuth Token** (format: `xoxb-...`).

## Setup

1. **Place Your Script:**
   Put the `due.py` script in a directory of your choice, for example:
   ```
   /path/to/your/project/due.py
   ```

2. **Configure the Script:**
   Open `due.py` and update:
   - `SLACK_TOKEN = "xoxb-..."` with your actual Slack Bot User OAuth Token.
   - `CHANNEL = "#anki-reminders"` or another Slack channel or user ID to receive the message.

3. **Test the Script:**
   Ensure Anki is running and AnkiConnect is active:
   ```bash
   python /path/to/your/project/due.py
   ```
   If successful, a Slack message will appear in the specified channel with your due card count.

## Scheduling with Cron

1. **Locate `conda.sh`:**
   Make sure you know where your `conda.sh` script is located. A common location:
   ```
   /opt/miniconda3/etc/profile.d/conda.sh
   ```
   Adjust if necessary.

2. **Add a Cron Job:**
   Open your crontab:
   ```bash
   crontab -e
   ```
   
   Add an entry to run daily at 8:00 AM:
   ```bash
   SHELL=/bin/bash
   0 8 * * * /bin/bash -c "source /opt/miniconda3/etc/profile.d/conda.sh && conda activate anki_slack_reminder && python '/path/to/your/project/due.py'" >> /tmp/anki_slack_reminder.log 2>&1
   ```

   This line:
   - Sets the shell to `bash`.
   - Sources `conda.sh` so `conda` commands are available.
   - Activates the `anki_slack_reminder` environment.
   - Runs the `due.py` script.
   - Redirects output and errors to `/tmp/anki_slack_reminder.log`.

3. **Test the Cron Job:**
   Temporarily adjust the time to a few minutes in the future, wait, and check:
   ```bash
   cat /tmp/anki_slack_reminder.log
   ```
   Review Slack for a new message and see if any errors were logged.

## Troubleshooting
- **No Slack Message:** Check that:
  - The bot is in the specified channel.
  - The channel name or ID is correct.
  - The Slack token is correct and the bot has `chat:write` permission.
- **`channel_not_found` Error:**  
  Invite the bot to the channel (`/invite @YourBotName`) or use a public channel.
- **AnkiConnect Issues:**  
  Ensure Anki is open. Test AnkiConnect:
  ```bash
  curl http://localhost:8765 -X POST -d '{"action":"version","version":6}'
  ```
- **Conda or Path Errors:**  
  If `conda.sh` isn’t found, run:
  ```bash
  find /opt -name conda.sh
  ```
  and update the cron job path accordingly.

## Customization
- **Message Format:**  
  Modify the Slack message in `due.py` to include more details, such as deck names or tags.
- **Scheduling:**  
  Change the cron schedule to suit your daily routine.
- **Environment:**  
  If not using conda, you can omit `conda.sh` and `conda activate` steps and call `python` directly, or use `virtualenv`.

## License
This project is licensed under the [MIT License](LICENSE).

---

By following these steps, you’ll have a Slack bot that posts daily reminders about your due Anki cards, helping you stay consistent with your reviews.