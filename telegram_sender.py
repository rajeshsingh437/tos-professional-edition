import os
import sys
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID") or 12345678)
API_HASH = os.getenv("TELEGRAM_API_HASH") or "your_api_hash"
TARGET_GROUP = os.getenv("TELEGRAM_TARGET_GROUP") or "TargetGroupNameOrID"

SESSION_NAME = "trade_user"

async def send_signal_to_group(text: str, target: str | int | None = None):
    """Sends a message to the group exactly as if you typed it in Telegram."""
    chat = target or TARGET_GROUP
    chat_target = int(chat) if str(chat).lstrip("-").isdigit() else chat
    
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        await client.send_message(chat_target, text)
        print(f"\n[SENT TO TELEGRAM]: '{text}' -> {chat_target}")

def send_signal(text: str, target: str | int | None = None):
    """Synchronous wrapper for easy import into other modules."""
    return asyncio.run(send_signal_to_group(text, target))

async def interactive_cli():
    print("\n" + "=" * 45)
    print("      AEGIS TELEGRAM SIGNAL SENDER")
    print("=" * 45)
    print(f"Target Chat ID: {TARGET_GROUP}")
    print("\nSelect an action:")
    print("  1. BUY CE")
    print("  2. BUY PE")
    print("  3. EXIT")
    print("  4. Send Safe Test Message ('Test connection - please ignore')")
    print("  5. Send Custom Text")
    print("  0. Cancel / Quit")
    print("-" * 45)
    
    choice = input("Enter choice (0-5): ").strip()
    
    if choice == "1":
        await send_signal_to_group("BUY CE")
    elif choice == "2":
        await send_signal_to_group("BUY PE")
    elif choice == "3":
        await send_signal_to_group("EXIT")
    elif choice == "4":
        await send_signal_to_group("Test connection - please ignore")
    elif choice == "5":
        custom = input("Enter custom message to send: ").strip()
        if custom:
            await send_signal_to_group(custom)
    else:
        print("Cancelled.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If passed via command line: python telegram_sender.py "BUY CE"
        msg = " ".join(sys.argv[1:])
        asyncio.run(send_signal_to_group(msg))
    else:
        # Interactive mode
        asyncio.run(interactive_cli())


