import os
from dotenv import load_dotenv
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables
load_dotenv()

# Configuration
ANKI_URL = os.getenv('ANKI_URL', 'http://127.0.0.1:8765')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL = os.getenv('SLACK_CHANNEL', 'anki-reminders')

if not SLACK_BOT_TOKEN:
    raise ValueError("SLACK_BOT_TOKEN environment variable is not set")

try:
    # Step 1: Find due cards
    find_cards_payload = {
        "action": "findCards",
        "version": 6,
        "params": {
            "query": "is:due"
        }
    }
    due_cards_response = requests.post(ANKI_URL, json=find_cards_payload)
    due_cards_response.raise_for_status()
    due_cards_data = due_cards_response.json()
    due_cards = due_cards_data.get("result", [])
    due_count = len(due_cards)

    # If there are due cards, retrieve their details
    if due_count > 0:
        cards_info_payload = {
            "action": "cardsInfo",
            "version": 6,
            "params": {
                "cards": due_cards
            }
        }
        cards_info_response = requests.post(ANKI_URL, json=cards_info_payload)
        cards_info_response.raise_for_status()
        cards_info_data = cards_info_response.json()
        card_infos = cards_info_data.get("result", [])

        # Extract the front field from each due card
        due_card_prompts = []
        for card in card_infos:
            front_field = card["fields"]["Front"]["value"]
            due_card_prompts.append(front_field.strip())

        # Construct a Slack message listing each due card's front field
        message = f"You have {due_count} Anki cards due:\n"
        for prompt in due_card_prompts:
            message += f"- {prompt}\n"
    else:
        message = "No Anki cards due!"

    # Step 2: Send the message to Slack
    client = WebClient(token=SLACK_BOT_TOKEN)
    response = client.chat_postMessage(channel=CHANNEL, text=message)
    
except requests.RequestException as e:
    print(f"Error connecting to Anki: {str(e)}")
except SlackApiError as e:
    print(f"Error posting to Slack: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
