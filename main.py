import asyncio
import nest_asyncio
nest_asyncio.apply()

from telethon import TelegramClient, events, errors
from parsing_trading_signal import parse_trading_signals
from instrument_key import convert_instrument
import json
from place_order import place_order

# Your API credentials and bot token
api_id = 1234
api_hash = 'hash'
bot_token = 'token'

async def main():
    while True:
        try:
            # Using None creates an in-memory session (won't persist between restarts)
            client = TelegramClient(None, api_id, api_hash)
            await client.start(bot_token=bot_token)
            print("Bot started successfully.")

            @client.on(events.NewMessage)
            async def handler(event):
                try:
                    print("New message received:")
                    # parse_trading_signals returns a JSON string, so convert it to a Python object.
                    parsed_signals_json = await asyncio.to_thread(parse_trading_signals, event.raw_text)
                    parsed_signals = json.loads(parsed_signals_json)
                    
                    # If parsed_signals is a list, process each signal.
                    # if isinstance(parsed_signals, list):
                    #     # for signal in parsed_signals:
                    #     if 'instrument' in parsed_signals:
                    #         parsed_signals['instrument'] = convert_instrument(parsed_signals['instrument'])
                    #     print(parsed_signals)
                    # Otherwise, if it's a single dictionary, update it directly.
                    if isinstance(parsed_signals, dict):
                        if 'instrument' in parsed_signals:
                            parsed_signals['instrument'], parsed_signals['lot_size'] = convert_instrument(parsed_signals['instrument'])
                        print(parsed_signals)
                        place_order(parsed_signals)
                    else:
                        print("Parsed signals are in an unexpected format:", parsed_signals)
                except Exception as e:
                    print("Error processing message:", e)

            # Run the client until it disconnects (this call blocks)
            await client.run_until_disconnected()
        except Exception as e:
            print("Client error:", e)
            print("Restarting client in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
