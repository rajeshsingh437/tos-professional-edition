import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

# You can either set these in a .env file or fill them in directly here
API_ID = int(os.getenv("TELEGRAM_API_ID") or 12345678)
API_HASH = os.getenv("TELEGRAM_API_HASH") or "your_api_hash"

SESSION_NAME = "trade_user"

async def main():
    if API_ID == 12345678 or API_HASH == "your_api_hash":
        print("[ERROR] Please replace API_ID and API_HASH with your real credentials first!")
        return

    print("Connecting to Telegram...")
    # TelegramClient context manager automatically calls start() on entry and disconnect() on exit
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print("\n[SUCCESS] Telegram Session successfully created and saved as 'trade_user.session'!\n")

        print("--- Available Groups & Channels ---")
        print(f"{'Title':<35} | {'Chat / Group ID'}")
        print("-" * 60)
        found = False
        async for dialog in client.iter_dialogs(limit=30):
            if dialog.is_group or dialog.is_channel:
                print(f"{dialog.title:<35} | {dialog.id}")
                found = True

        if not found:
            print("No groups or channels found in recent 30 dialogs.")
        print("-" * 60)
        print("Copy the 'Chat / Group ID' for your target group.")

if __name__ == "__main__":
    asyncio.run(main())

